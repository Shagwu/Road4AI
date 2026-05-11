#!/usr/bin/env python3
import os
import time
import fcntl
from contextlib import contextmanager

LOCK_DIR = ".locks"

@contextmanager
def file_lock(lock_name):
    """
    Simple file-based advisory lock to prevent race conditions in swarms.
    """
    if not os.path.exists(LOCK_DIR):
        os.makedirs(LOCK_DIR, exist_ok=True)
        
    lock_path = os.path.join(LOCK_DIR, f"{lock_name}.lock")
    
    with open(lock_path, "w") as f:
        try:
            # Acquire an exclusive lock (non-blocking wait)
            fcntl.flock(f, fcntl.LOCK_EX)
            yield
        finally:
            # Release the lock
            fcntl.flock(f, fcntl.LOCK_UN)

if __name__ == "__main__":
    # Example usage:
    # with file_lock("current-queue"):
    #     # Read and write to state/current-queue.json safely
    #     pass
    print(f"Locker utility initialized in {LOCK_DIR}")
