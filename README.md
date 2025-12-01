# intuit-build-challenge
All code lives under the top-level `src` directory, and their corresponding tests can be found under the `tests` directory

## producer-consumer

### Description
This module implements a classic **producer–consumer** pattern with a fixed-capacity, thread-safe buffer.

- The `BlockingBuffer` class implements a bounded queue with thread synchronization.
  - If the buffer is full, calls to `put()` block the producer until space is available.
  - If the buffer is empty, calls to `take()` block the consumer until an item is available.
  - Synchronization is implemented using Python’s `threading.Condition` (wait/notify mechanism).

- The `Producer` and `Consumer` classes are built on top of the `threading.Thread` API and operate concurrently on the shared buffer:
  - `Producer` reads from a source container and puts items into the buffer.
  - `Consumer` takes items from the buffer and writes them into a destination container.
  - A special sentinel (poison pill) is used to signal the consumer to stop once production is complete.

### Running example code
1. Navigate to the producer_consumer directory

2. Inside the directory, run `python3 -m producer_consumer.main`

This will start a producer and consumer, transfer items through the blocking buffer, and print the results.

### Running tests:
1. Run `pytest tests/test_producer_consumer.py` at the root directory


## data_analysis

### Description




### To run all tests:
Run `pytest -q` at the root directory


