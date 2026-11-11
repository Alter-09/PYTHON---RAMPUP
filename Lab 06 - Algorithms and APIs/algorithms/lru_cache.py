"""Least Recently Used (LRU) Cache using collections.OrderedDict.

Time complexity: O(1) average for both get() and put() operations.
Sace complexity: O(c) where c is the fixed capcacity.
"""

from numpy.f2py.auxfuncs import throw_error
from collections import OrderedDict
from typing import Any

class LRUCache:
    """O(1) LRU cache leveraging OrderedDict double hashing & linked list behavior"""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self.capacity = capacity
        self.cache: OrderedDict[Any, Any] = OrderedDict()
    
    def get(self, key: Any) -> Any:
        """Retrieve key value and mark as most recently used. O(1) time."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: Any, value: Any) -> None:
        """Insert/update key and evict Least recently used item if full. O(1) time."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value

        if len(self.cache) > self.capacity:
            #Evict first item (APPLY LRU METHOD)
            self.cache.popitem(last=False)