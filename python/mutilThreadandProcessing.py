import concurrent.futures
import logging
import multiprocessing
import os
import time
from typing import List, Any

# Configure logging for thread-safe output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(processName)s-%(threadName)s) %(message)s"
)

def worker_logic(item: Any) -> Any:
    """
    Core business logic for the worker. 
    Handles individual item processing with error isolation.
    """
    try:
        # Simulate workload
        time.sleep(0.5)
        return f"Processed {item} in PID {os.getpid()}"
    except Exception as e:
        logging.error(f"Error processing item {item}: {e}")
        return None

def execute_io_bound_tasks(data: List[Any], max_workers: int = None):
    """
    Template for I/O bound tasks using ThreadPoolExecutor.
    Ideal for network requests, file I/O, or database queries.
    """
    logging.info("Starting ThreadPoolExecutor...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use as_completed to handle results as they finish
        future_to_item = {executor.submit(worker_logic, item): item for item in data}
        for future in concurrent.futures.as_completed(future_to_item):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as exc:
                logging.error(f"Generated an exception: {exc}")
    return results

def execute_cpu_bound_tasks(data: List[Any]):
    """
    Template for CPU bound tasks using ProcessPoolExecutor.
    Ideal for heavy computations, bypassing the Global Interpreter Lock (GIL).
    """
    logging.info("Starting ProcessPoolExecutor...")
    # Default max_workers is os.cpu_count()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Use map for ordered results and simpler syntax
        results = list(executor.map(worker_logic, data))
    return results

if __name__ == "__main__":
    test_data = [1, 2, 3, 4, 5]

    # I/O Bound Example
    io_results = execute_io_bound_tasks(test_data)
    logging.info(f"I/O Results: {io_results}")

    # CPU Bound Example
    # Note: Multiprocessing requires the __main__ guard on Windows
    cpu_results = execute_cpu_bound_tasks(test_data)
    logging.info(f"CPU Results: {cpu_results}")
