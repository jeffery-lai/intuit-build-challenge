import threading
import time
from .blocking_buffer import BlockingBuffer


class Producer(threading.Thread):
    """
    Producer thread:
    Reads from a source list and pushes items into the blocking buffer.
    """

    def __init__(self, source, buffer, poison_pill):
        super().__init__()
        self.source = source
        self.buffer = buffer
        self.poison_pill = poison_pill

    def run(self):
        for item in self.source:
            print(f"[Producer] Producing {item}")
            self.buffer.put(item)
            time.sleep(0.1)  # Pause to simulate work

        # Send poison pill to stop the consumer
        self.buffer.put(self.poison_pill)
        print("[Producer] Sent poison pill, finished producing.")


class Consumer(threading.Thread):
    """
    Consumer thread:
    Reads from the blocking buffer and processes items into a destination list.
    """

    def __init__(self, buffer, destination, poison_pill):
        super().__init__()
        self.buffer = buffer
        self.destination = destination
        self.poison_pill = poison_pill

    def run(self):
        while True:
            item = self.buffer.take()

            if item is self.poison_pill:
                print("[Consumer] Received poison pill. Stopping.")
                break

            print(f"[Consumer] Consuming {item}")
            self.destination.append(item)
            time.sleep(0.2)  # Simulate work
