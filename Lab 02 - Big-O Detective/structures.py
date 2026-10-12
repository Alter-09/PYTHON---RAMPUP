"""
Data Structures Lab for Lab 02: Big-O Detective.
Implements optimized data structures using the Python standard library:
- Word frequency counter comparison (Counter vs dict.get)
- FIFO Queue and LIFO Stack using collections.deque
- LRU Cache using collections.OrderedDict
- Item grouping using collections.defaultdict
"""

from collections import Counter, OrderedDict, defaultdict, deque
from typing import Any, Hashable

# ============================================================================
# 1. Word Frequency Counting (Counter vs dict.get)
# ============================================================================
# ============================================================================
# Part A - Complexity Analysis Fragments
# ============================================================================

def has_duplicates_nested(nums: list[int]) -> bool:
    """Fragment 1: Nested-loop duplicate check.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False
def has_duplicates_set(nums: list[int]) -> bool:
    """Fragment 2: Set-based duplicate check.
    
    Time Complexity: O(n) average
    Space Complexity: O(n)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
def two_sum_dict(nums: list[int], target: int) -> tuple[int, int] | None:
    """Fragment 3: Two-sum using a dictionary (hash map).
    
    Time Complexity: O(n) average
    Space Complexity: O(n)
    """
    seen: dict[int, int] = {}  # maps value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

    # ============================================================================
# Part B - Structure Choice Implementations
# ============================================================================

# 1. Word frequency counter comparison (Counter vs dict.get)
def count_words_counter(text: str) -> Counter[str]:
    """Count word frequencies using collections.Counter."""
    return Counter(text.lower().split())


def count_words_dict_get(text: str) -> dict[str, int]:
    """Count word frequencies using a standard dict and .get()."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


# 2. FIFO Queue and LIFO Stack with collections.deque
class FIFOQueue:
    """FIFO (First-In, First-Out) Queue implemented with collections.deque.
    
    Why deque instead of list?
    - list.pop(0) requires shifting all remaining elements left: O(n).
    - deque.popleft() is O(1) guaranteed because it uses a doubly linked list of blocks.
    """

    def __init__(self) -> None:
        self._items: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Add item to back of queue. Complexity: O(1)."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return item from front of queue. Complexity: O(1)."""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.popleft()

    def peek(self) -> Any:
        """Inspect the front item without removing it. Complexity: O(1)."""
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class LIFOStack:
    """LIFO (Last-In, First-Out) Stack implemented with collections.deque.
    
    Both push and pop operate in O(1) time without list dynamic array resizing spikes.
    """

    def __init__(self) -> None:
        self._items: deque[Any] = deque()

    def push(self, item: Any) -> None:
        """Push item onto stack. Complexity: O(1)."""
        self._items.append(item)

    def pop(self) -> Any:
        """Pop item off stack. Complexity: O(1)."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Inspect top item without removing it. Complexity: O(1)."""
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


# 3. LRU Cache using collections.OrderedDict
class LRUCache:
    """Least Recently Used (LRU) Cache backed by collections.OrderedDict.
    
    Complexities:
    - get(key): O(1) average
    - put(key, value): O(1) average
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity: int = capacity
        self.cache: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable) -> Any:
        """Retrieve key value and mark as most recently used. Complexity: O(1) avg."""
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Hashable, value: Any) -> None:
        """Insert/update value and evict LRU item if capacity is exceeded. Complexity: O(1) avg."""
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return

        if len(self.cache) >= self.capacity:
            # Evict least recently used item (the first item)
            self.cache.popitem(last=False)

        self.cache[key] = value


# 4. Group items with collections.defaultdict(list)
def group_items_by_key(items: list[dict[str, Any]], group_key: str) -> dict[str, list[dict[str, Any]]]:
    """Group list of dict records by a given key using collections.defaultdict(list).
    Complexity: O(n) average.
    """
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        val = str(item.get(group_key, "unknown"))
        grouped[val].append(item)
    return dict(grouped)

