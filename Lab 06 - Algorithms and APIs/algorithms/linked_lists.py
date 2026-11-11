"""
Singly linked list implementation aand inversion algorithm.

Time complexity: O(n) Single traversal of the linked list.
Space complexity: O(1) Iterative pointer manipulation in constant memory.

"""

from typing import Any, Optional

class Node:
    """ Represents a single node in a singly linked list. """

    def __init__(self, value: Any, next_node: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next_node

class LinkedList:
    """Singly linked list with iterative reversal capability."""

    def __init__(self) -> None:
        self.head: Optional [Node] = None

    def append(self, value: Any) -> None:
        """Append an item to the end of the list."""
        if not self.head:
            self.head = Node(value) # If the list is empty, the new node becomes the head
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(value)
        #Step into the last node to append the new one

    def reverse(self) -> None:
        """Reversed the linked list in-place
        
        Time complexity: O(n) - Single pass through all nodes.
        Space complexity: O(1) - Constant auxiliary memory by rewiring pointers.
        """
        # Initialize prev to None so the reversed list's new tail correctly points to None.
        # (Fix: was previously initialized to the class `Node`, which caused AttributeError)
        prev: Optional[Node] = None
        current = self.head

        while current is not None:
            next_node = current.next    # Preserve reference to the next node before overwriting
            current.next = prev         # Reverse the link direction to point backwards
            prev = current              # Advance prev pointer to current node
            current = next_node         # Advance current pointer to next node

        # The loop terminates when current is None; prev now points to the new head
        self.head = prev
    
    def to_list(self) -> list[Any]:
        """Convert linked list elements into a standard Python list for verification."""
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

