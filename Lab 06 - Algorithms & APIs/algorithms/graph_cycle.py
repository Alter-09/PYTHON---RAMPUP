"""Directed graph cycle detection using Depth-First Search (DFS)

Time Complexity: O(V + E) where V is vertices and E is edges.
Space Complexity: O(V) for visited and active recursion stack tracking.
"""
from typing import List, Set, Dict

def has_cycle(graph: Dict[int, List[int]]) -> bool:
    
    visited: Set[int] = set()
    rec_stack: Set[int] = set()

    def dfs(node:int) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False