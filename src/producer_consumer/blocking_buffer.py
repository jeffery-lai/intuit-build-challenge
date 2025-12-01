import threading


class BlockingBuffer:
    """
    A thread-safe bounded buffer implementing blocking put() and take()
    using a Condition variable. Demonstrates:
    - thread synchronization
    - wait/notify
    - concurrent access protection
    """

    def __init__(self, capacity=10):
        # Ensure capacity is positive
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.buffer = []
        self.condition = threading.Condition()

    def put(self, item):
        """
        Put an item into the buffer.
        Blocks if the buffer is full.
        """
        with self.condition:
            # Wait if buffer is full
            while len(self.buffer) >= self.capacity:
                self.condition.wait()

            self.buffer.append(item)

            # Notify a waiting consumer that an item is available
            self.condition.notify_all()

    def take(self):
        """
        Take an item from the buffer.
        Blocks if the buffer is empty.
        """
        with self.condition:
            # Wait if buffer is empty
            while len(self.buffer) == 0:
                self.condition.wait()

            item = self.buffer.pop(0)

            # Notify a waiting producer that space is free
            self.condition.notify_all()

            return item
