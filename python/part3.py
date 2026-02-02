from functools import wraps
import time
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# 1. Basic Decorator
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hi():
    print("Hi!")

# 2. Decorator functioning with arguments and return values using @wraps
def log_execution(func):
    @wraps(func) # Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_execution
def add(a, b):
    """Adds two numbers."""
    return a + b

# 3. Decorator taking arguments (High Order Decorator)
def repeat(num_times):
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name):
    print(f"Hello {name}")

# 4. Timer Decorator (Useful for performance monitoring)
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return result
    return wrapper

@timer
def heavy_computation():
    sum([i**2 for i in range(100000)])

# 5. Retry Decorator (Robustness for flaky operations)
def retry(max_retries=3, delay=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Error {e}. Retrying {retries}/{max_retries}...")
                    time.sleep(delay)
            raise Exception("Max retries exceeded")
        return wrapper
    return decorator_retry

@retry(max_retries=2, delay=0.1)
def unstable_network_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network failure")
    return "Success"

# 6. Class Decorator
# Adds a common method or property to a class
def add_str_method(cls):
    def new_str(self):
        return f"Instance of {cls.__name__} at {id(self)}"
    cls.__str__ = new_str
    return cls

@add_str_method
class MyObject:
    pass

# 7. Stateful Decorator (Using a class as a decorator)
class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)

@CountCalls
def say_something():
    print("Something")


if __name__ == "__main__":
    print("--- Basic Decorator ---")
    say_hi()

    print("\n--- Log Execution ---")
    print(add(5, 10))
    print(f"Function Name: {add.__name__}, Doc: {add.__doc__}")

    print("\n--- Decorator with Arguments ---")
    greet("World")

    print("\n--- Timer ---")
    heavy_computation()

    print("\n--- Retry ---")
    try:
        print(unstable_network_call())
    except Exception as e:
        print(e)
    
    print("\n--- Class Decorator ---")
    obj = MyObject()
    print(obj)

    print("\n--- Stateful Decorator ---")
    say_something()
    say_something()
