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