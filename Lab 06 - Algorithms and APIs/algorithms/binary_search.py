"""Binary Search and Integer Square Root. 

Time Complexity: O(log x) - Binary search search space halving. 
Space Complexity: O(1) - Constant auxiliary storage.
""" 

def integer_sqrt(x: int) -> int:
    """Compute floor of square root of x using binary search (floor(sqrt(x))). 
    
    Time Complexity: O(log x) 
    Space Complexity: O(1) 
    """ 
    
    if x < 0: 
        raise ValueError("Cannot calculate square root of negative number") 
    if x < 2: 
        return x 
        
    left, right = 1, x // 2
    ans = 0 
    
    while left <= right: 
        mid = (left + right) // 2 
        square = mid * mid 
        
        if square == x: 
            return mid 
        elif square < x: 
            ans = mid # mid is valid candidate 
            left = mid + 1 
        else: 
            right = mid - 1 
            
    return ans