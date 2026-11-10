""" First non-repeating Character in a String using Frequency Maps


"""

from collections import Counter

def first_non_repeating_char(s: str) -> int:

    counts = Counter(s)

    for index, char in enumerate(s):
        if counts[char] == 1:
            return index
    return -1