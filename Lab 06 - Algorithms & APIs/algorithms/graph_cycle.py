"""Graph cycle detection using DFS and Visited Sets."""

from matplotlib.font_manager import _normalize_weight
def has_cycle(graph: dict [int, list[int]]) -> bool:
    """
    Detect if a directed graph contains a cycle using DFS

    Time complexity: O(V + E) Where V is vertices and E is edges.
    Space complexity: O(V) for visited and recursion stack sets.
    """

    visited: set[int] = set()
    rec_stack: set[int] = set()

    def dfs(node: int) -> bool:
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


