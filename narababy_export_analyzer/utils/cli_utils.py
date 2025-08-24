import os

def display_success(message: str) -> str:
    print("{0:.<10}{1}".format("[OK]", message))

def display_failure(message: str) -> str:
    print("{0:.<10}{1}".format("[FAIL]", message))

def get_elapsed_time(start: float, end: float) -> float:
    """Returns elapsed time in milliseconds."""

    return (end - start) * 1000

