# Author: Harshiv Chhabra
# Date: 2023-04-26
# Description: This script demonstrates the use of decorators in Python for a
# technical assessment at BIPP, Indian School of Business. It includes a
# timing_decorator to measure execution time, and a caching_decorator to
# store and reuse the results of a function.

import time

# Timing decorator to measure the execution time of a function
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        # Record the start time
        start_time = time.time()

        # Call the original function
        result = func(*args, **kwargs)

        # Record the end time
        end_time = time.time()

        # Calculate and print the time taken for execution
        print(f"{func.__name__} took {end_time - start_time:.10f} seconds to run.")

        return result
    return wrapper

# Caching decorator to store and reuse the results of a function
def caching_decorator(func):
    cache = {}

    def wrapper(*args):
        # Convert the list to a tuple to use as a cache key
        key = tuple(args[0])

        # If the key is in the cache, return the cached result
        if key in cache:
            return cache[key]

        # Otherwise, call the original function and store the result in the cache
        result = func(*args)
        cache[key] = result

        return result
    return wrapper

# Apply both decorators to the sum_integers function
@timing_decorator
@caching_decorator
def sum_integers(numbers):
    return sum(numbers)

# Call the sum_integers function with a list of integers
integers = [100, 200, 3000, 41231231, 500]

print("First call:")
result = sum_integers(integers)
print(f"Sum of integers: {result}\n")

print("Second call:")
result = sum_integers(integers)
print(f"Sum of integers: {result}\n")