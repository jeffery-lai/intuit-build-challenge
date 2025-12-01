# Intuit Build Challenge
All Python code lives under the top-level `src` directory, and corresponding tests live under the `tests` directory

## Assignment 1: producer_consumer

### Description
This module implements a classic producer–consumer pattern with a fixed-capacity, thread-safe buffer.

- The `BlockingBuffer` class implements a bounded queue with thread synchronization.
  - If the buffer is full, calls to `put()` block the producer until space is available.
  - If the buffer is empty, calls to `take()` block the consumer until an item is available.
  - Synchronization is implemented using Python’s `threading.Condition` (wait/notify mechanism).

- The `Producer` and `Consumer` classes are built on top of the `threading.Thread` API and operate concurrently on the shared buffer:
  - `Producer` reads from a source container and puts items into the buffer.
  - `Consumer` takes items from the buffer and writes them into a destination container.
  - A special sentinel (poison pill) is used to signal the consumer to stop once production is complete.

### Running example code
1. Navigate into the `src` directory

2. Inside the directory, run `python3 -m producer_consumer.main`

This will start a producer and consumer, transfer items through the blocking buffer, and print the results.

### Running tests:
1. Run `pytest tests/test_producer_consumer.py` at the root directory


## Assignment 2: data_analysis

### Description
This module reads a CSV file of sales records and performs several analytical queries, such as:

- Total revenue across all records  
- Revenue grouped by region and by product  
- Quantity sold per category  
- Average order value per day (grouped by date and order)  
- Top N products by revenue  
- Nested revenue breakdown by region → category  
- Best-selling product by quantity  

A dataset was generated with consideration of the following guidelines:
- Represents a common business use case with meaningful product categories.
- Includes multiple regions, products, and categories.
- Uses simple, human-readable types so that the focus stays on functional/stream-style processing rather than handling edge cases.

### Running code on dataset
1. Navigate into the `src` directory

2. Inside the directory, run `python3 -m data_analysis.main`

This will load CSV data and print a summary including total revenue, breakdowns by category, and other analytics.
The expected console output can be found in `output.txt` under the `data_analysis` directory

### Running tests:
1. Run `pytest tests/test_data_analysis.py` at the root directory


## To run all tests:
Run `pytest -q` at the root directory
