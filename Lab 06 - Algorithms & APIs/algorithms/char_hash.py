""" First non-repeating Character in a String using Frequency Maps

Time Complexity: O(n) - Two passes over the String (first for counting the elements, the second for index search)
Space Complexity: O(1) - Frequency hash map capped by alphabet size (max 26 for English lowercase)
"""

from collections import Counter

def first_non_repeating_char(s: str) -> int:
    """Find index of first unique character in the string. Return -1 if not exists 
    
    Time Complexity: O(n)
    Space Complexity: O(1) auxiliary space (character set bounds).
    """

    counts = Counter(s)

    for index, char in enumerate(s):
        if counts[char] == 1:
            return index
    return -1