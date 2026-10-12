# Lab 02: Big-O Detective & Data Structures

---

## Part A - Complexity Analysis

### 1. Nested-Loop Duplicate Check
```python
def has_duplicates_nested(nums: list[int]) -> bool:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False
```
* **Time Complexity**: **$\mathcal{O}(n^2)$**
* **Space Complexity**: **$\mathcal{O}(1)$**
* **Operation Count & English Explanation**:
  * For an input list of size $n$, the outer loop executes $n$ times.
  * In iteration $i$, the inner loop executes $(n - 1 - i)$ times.
  * Total comparisons in the worst case (when no duplicates exist or duplicates are at the very end):
    $$\sum_{i=0}^{n-1} (n - 1 - i) = (n - 1) + (n - 2) + \dots + 1 + 0 = \frac{n(n - 1)}{2} = \frac{1}{2}n^2 - \frac{1}{2}n$$
  * Dominant term is $n^2$, ignoring constants $\implies \mathcal{O}(n^2)$ operations. No additional memory is allocated ($\mathcal{O}(1)$).

---

### 2. Set-Based Duplicate Check
```python
def has_duplicates_set(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```
* **Time Complexity**: **$\mathcal{O}(n)$** (average case), $\mathcal{O}(n^2)$ worst-case under theoretical hash collision collapse.
* **Space Complexity**: **$\mathcal{O}(n)$**
* **Operation Count & English Explanation**:
  * The loop iterates through $n$ elements once.
  * In each iteration, `num in seen` is a hash-table lookup requiring $\mathcal{O}(1)$ average operations.
  * `seen.add(num)` is a hash-table insertion requiring $\mathcal{O}(1)$ average operations.
  * Total operations: $\approx 2n \implies \mathcal{O}(n)$ linear time.
  * Memory: In the worst case, the hash set stores all $n$ distinct elements $\implies \mathcal{O}(n)$ space.

---

### 3. Two-Sum with Dictionary (Hash Map)
```python
def two_sum_dict(nums: list[int], target: int) -> tuple[int, int] | None:
    seen = {}  # maps number -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None
```
* **Time Complexity**: **$\mathcal{O}(n)$** (average case)
* **Space Complexity**: **$\mathcal{O}(n)$**
* **Operation Count & English Explanation**:
  * Traverses the list of size $n$ with a single loop.
  * Each step performs:
    1. One subtraction: `target - num` ($\mathcal{O}(1)$).
    2. One dictionary lookup: `complement in seen` ($\mathcal{O}(1)$ average).
    3. One dictionary insertion: `seen[num] = i` ($\mathcal{O}(1)$ average).
  * Total operations: at most $3n$ elementary steps $\implies \mathcal{O}(n)$ linear time.
  * Space complexity is $\mathcal{O}(n)$ because `seen` stores up to $n$ key-value pairs.

---

