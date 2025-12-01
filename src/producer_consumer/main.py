from .blocking_buffer import BlockingBuffer
from .producer_consumer import Producer, Consumer


def main():
    # Example data to be processed
    source = [1, 2, 3, 4, 5]
    destination = []
    poison_pill = object()

    buffer = BlockingBuffer(capacity=2)

    # Create producer and consumer threads
    producer = Producer(source, buffer, poison_pill)
    consumer = Consumer(buffer, destination, poison_pill)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print("\nFinal output:", destination)


if __name__ == "__main__":
    main()
