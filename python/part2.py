import asyncio
import time
import random

# 1. Basic Async/Await
async def say_hello_async():
    print("Hello")
    await asyncio.sleep(1) # Simulating non-blocking I/O
    print("World")

# 2. Coroutine returning a value
async def fetch_data(id):
    print(f"Fetching data for {id}...")
    await asyncio.sleep(random.uniform(0.5, 2.0)) # Simulate network delay
    print(f"Data for {id} received")
    return {"id": id, "data": f"Sample Data {id}"}

# 3. Running concurrently with asyncio.gather
async def main_concurrent():
    start_time = time.perf_counter()
    
    # Schedule three calls *concurrently*:
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3),
    )
    
    end_time = time.perf_counter()
    print(f"Results: {results}")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

# 4. Async Context Manager (Simulating a database connection)
class AsyncDatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    async def __aenter__(self):
        print(f"Connecting to {self.db_name}...")
        await asyncio.sleep(0.5)
        print(f"Connected to {self.db_name}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print(f"Closing connection to {self.db_name}...")
        await asyncio.sleep(0.5)
        print(f"Connection closed")

    async def query(self, sql):
        print(f"Executing query: {sql}")
        await asyncio.sleep(0.2)
        return f"Result for {sql}"

async def database_example():
    async with AsyncDatabaseConnection("UserDB") as db:
        result = await db.query("SELECT * FROM users")
        print(result)

# 5. Async Iterator (Streaming data)
class AsyncDataStream:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count < self.limit:
            await asyncio.sleep(0.1) # Simulate fetching next chunk efficiently
            self.count += 1
            return f"Chunk {self.count}"
        else:
            raise StopAsyncIteration

async def stream_example():
    print("\nStreaming Data:")
    async for chunk in AsyncDataStream(3):
        print(chunk)

# 6. Timeouts
async def slow_operation():
    await asyncio.sleep(5)
    return "Finished slow operation"

async def timeout_example():
    try:
        # Wait for at most 2 seconds
        res = await asyncio.wait_for(slow_operation(), timeout=2.0)
        print(res)
    except asyncio.TimeoutError:
        print("\nOperation timed out!")

# Main entry point to run different examples
async def main():
    print("--- Basic Async ---")
    await say_hello_async()
    
    print("\n--- Concurrent Execution ---")
    await main_concurrent()
    
    print("\n--- Async Context Manager ---")
    await database_example()
    
    print("\n--- Async Iterator ---")
    await stream_example()

    print("\n--- Timeout Handling ---")
    await timeout_example()

if __name__ == "__main__":
    asyncio.run(main())
