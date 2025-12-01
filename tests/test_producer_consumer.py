import threading
import time
import pytest

from producer_consumer.blocking_buffer import BlockingBuffer
from producer_consumer.producer_consumer import Producer, Consumer


# ---------- BlockingBuffer Tests ----------

def test_invalid_capacity_raises():
    """
    Check invalid capacity raises ValueError.
    """
    with pytest.raises(ValueError):
        BlockingBuffer(0)

    with pytest.raises(ValueError):
        BlockingBuffer(-5)


def test_put_and_take():
    """
    Test basic put and take buffer operations.
    """
    buffer = BlockingBuffer(capacity=3)

    buffer.put(1)
    buffer.put(2)
    buffer.put(3)

    assert buffer.take() == 1
    assert buffer.take() == 2
    assert buffer.take() == 3


def test_order_is_fifo():
    """
    Test that buffer keeps items in FIFO order.
    """
    buffer = BlockingBuffer(capacity=10)
    items = ["a", "b", "c", "d"]

    for item in items:
        buffer.put(item)

    results = [buffer.take() for _ in range(len(items))]
    assert results == items


def test_put_blocks_when_full():
    """
    Fill the buffer, then start a thread that tries to put another item.
    It should block until we free space in the buffer.
    """
    buffer = BlockingBuffer(capacity=1)
    put_completed = threading.Event()

    # Pre fill buffer
    buffer.put("first")

    def producer_task():
        buffer.put("second")
        put_completed.set()

    t = threading.Thread(target=producer_task)
    t.start()

    # Allow producer to start, put should be blocked
    time.sleep(0.1)
    assert not put_completed.is_set()

    # Free space in the buffer
    item = buffer.take()
    assert item == "first"

    # The blocked put should now complete
    t.join(timeout=1.0)
    assert not t.is_alive()
    assert buffer.take() == "second"


def test_take_blocks_when_empty_until_put():
    """
    Start a thread that calls take() on an empty buffer.
    It should block until we put an item into the buffer.
    """
    buffer = BlockingBuffer(capacity=1)
    take_completed = threading.Event()
    results = []

    def consumer_task():
        item = buffer.take()
        results.append(item)
        take_completed.set()

    t = threading.Thread(target=consumer_task)
    t.start()

    # Give the thread a moment, the take should be blocked
    time.sleep(0.1)
    assert not take_completed.is_set()

    # Put an item so the take can complete
    buffer.put("value")

    t.join(timeout=1.0)
    assert not t.is_alive()
    assert take_completed.is_set()
    assert results == ["value"]


# ---------- Producer–Consumer integration tests ----------

def test_all_items_transferred_in_order():
    """
    Producer should move all items from source to buffer,
    Consumer should move them from buffer to destination in the correct order.
    """
    source = list(range(10))
    destination = []

    buffer = BlockingBuffer(capacity=3)
    poison_pill = object()

    producer = Producer(source=source, buffer=buffer, poison_pill=poison_pill)
    consumer = Consumer(buffer=buffer, destination=destination, poison_pill=poison_pill)

    producer.start()
    consumer.start()

    # Wait for producer and consumer to complete
    producer.join(timeout=2.0)
    consumer.join(timeout=2.0)

    # Check threads are finished and data is correct
    assert not producer.is_alive()
    assert not consumer.is_alive()
    assert destination == source


def test_empty_source_results_in_empty_destination():
    source = []
    destination = []

    buffer = BlockingBuffer(capacity=2)
    poison_pill = object()

    producer = Producer(source=source, buffer=buffer, poison_pill=poison_pill)
    consumer = Consumer(buffer=buffer, destination=destination, poison_pill=poison_pill)

    producer.start()
    consumer.start()

    producer.join(timeout=2.0)
    consumer.join(timeout=2.0)

    # Check threads are finished and data is consistent
    assert not producer.is_alive()
    assert not consumer.is_alive()
    assert destination == []


def test_consumer_stops_on_poison_pill():
    """
    Explicitly verify that the consumer stops when it sees the poison pill.
    """
    source = [1, 2, 3]
    destination = []

    buffer = BlockingBuffer(capacity=2)
    poison_pill = object()

    producer = Producer(source=source, buffer=buffer, poison_pill=poison_pill)
    consumer = Consumer(buffer=buffer, destination=destination, poison_pill=poison_pill)

    producer.start()
    consumer.start()

    producer.join(timeout=2.0)
    consumer.join(timeout=2.0)

    # Check poison pill condition is triggered
    assert not consumer.is_alive()
    assert destination == source


def test_non_integer_items():
    """
    Ensure the pipeline can handle arbitrary Python objects.
    """

    class Dummy:
        def __init__(self, value):
            self.value = value

    source = [Dummy(i) for i in range(5)]
    destination = []

    buffer = BlockingBuffer(capacity=2)
    poison_pill = object()

    producer = Producer(source=source, buffer=buffer, poison_pill=poison_pill)
    consumer = Consumer(buffer=buffer, destination=destination, poison_pill=poison_pill)

    producer.start()
    consumer.start()

    producer.join(timeout=2.0)
    consumer.join(timeout=2.0)

    assert not producer.is_alive()
    assert not consumer.is_alive()

    # Check that all Dummy objects arrived with correct values
    assert len(destination) == len(source)
    assert [d.value for d in destination] == [s.value for s in source]
