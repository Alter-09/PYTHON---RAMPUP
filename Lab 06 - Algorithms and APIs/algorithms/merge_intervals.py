"""Merge Overlapping Intervals Algorithm. 
Time Complexity: O(n log n) - Dominated by initial sorting step. 
Space Complexity: O(n) - Output memory to store merged interval pairs.
 """ 
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]: 
    """Merge all overlapping intervals into a consolidated sequence. 
    
    Args: intervals: List of [start, end] integer intervals. 
    
    Returns: List of merged non-overlapping intervals. 
    """ 
    if not intervals: 
        return [] 
        
    # Sort intervals by starting point O(n log n) 
    intervals.sort(key=lambda x: x[0]) 
    # Seed the accumulator with the first interval [start, end]
    # (Fix: was `[intervals]`, which nested the entire list as a single 3D/2D element)
    merged: list[list[int]] = [intervals[0]] 
    
    for current in intervals[1:]: 
        prev_start, prev_end = merged[-1] 
        curr_start, curr_end = current 
        
        if curr_start <= prev_end: 
            # Overlap detected: extend end of previous interval to cover both
            # (Fix: index was `[4]`, corrected to `[1]` for [start, end])
            merged[-1][1] = max(prev_end, curr_end) 
        else:
            # No overlap: append current interval as a new disjoint range
            merged.append(current) 
        
    return merged
