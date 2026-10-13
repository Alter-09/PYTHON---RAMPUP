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

## Part B - Structure Choice

### 1. Word Frequencies in a Huge Text: `Counter` vs `dict.get`

* **Chosen Structure**: `collections.Counter`
* **Justification**:
  * **C-Level Optimization**: In CPython, `Counter` executes its inner frequency tallying loops in compiled C. In contrast, using `counts[w] = counts.get(w, 0) + 1` incurs Python bytecode interpreter overhead on every word lookup and addition.
  * **Memory & Streaming**: When processing massive files that exceed available RAM, `Counter.update()` can accept generators yielding chunks or lines from the file, aggregating counts on the fly without loading the whole dataset into memory.
  * **Top-$k$ Queries**: Finding the most frequent words with `Counter.most_common(k)` uses an internal `heapq.nlargest` algorithm requiring **$\mathcal{O}(n \log k)$** time, which is significantly faster and uses less memory than sorting the entire dictionary with `sorted()` in **$\mathcal{O}(n \log n)$** time.

---

### 2. FIFO Queue and LIFO Stack with `deque`: Why Not `list`?

* **FIFO Queue**:
  * **With `list`**: Enqueuing is `list.append(x)` ($\mathcal{O}(1)$ amortized), but dequeuing requires `list.pop(0)`. Because Python lists are dynamic contiguous arrays, removing the element at index `0` forces all remaining $(n - 1)$ elements to shift left in memory by one position. This is an **$\mathcal{O}(n)$** operation per dequeue, resulting in **$\mathcal{O}(n^2)$** total time for $n$ items.
  * **With `deque`**: `collections.deque` is implemented as a doubly linked list of fixed-size blocks (unrolled linked list). Both `append()` and `popleft()` operate with guaranteed **$\mathcal{O}(1)$** time complexity with zero element shifting.

* **LIFO Stack**:
  * **With `list`**: `list.append()` and `list.pop()` are amortized $\mathcal{O}(1)$. However, dynamic arrays must occasionally resize geometrically (over-allocation), triggering memory reallocation and block-copy bursts.
  * **With `deque`**: `deque.append()` and `deque.pop()` have strict, consistent **$\mathcal{O}(1)$** worst-case bounds without reallocation pauses, making it safer for real-time or low-latency workloads.

---

### 3. LRU Cache with `OrderedDict`

* **Implementation Mechanism**: Combines a hash map for key-value lookups with a doubly linked list to track access order.
* **Complexities**:
  * **`get(key)`**: **$\mathcal{O}(1)$ average time**. Performs a hash table lookup and updates recency order via `move_to_end(key)`, which only adjusts doubly-linked pointers in $\mathcal{O}(1)$ time.
  * **`put(key, value)`**: **$\mathcal{O}(1)$ average time**. Inserts or updates the entry in $\mathcal{O}(1)$. If the capacity is exceeded, evicts the least recently used element from the front via `popitem(last=False)` in $\mathcal{O}(1)$ pointer operations.
  * **Space Complexity**: **$\mathcal{O}(C)$**, where $C$ is the cache capacity.

---

### 4. Grouping Items with `defaultdict(list)`

* **Mechanism**: Creates an entry with an empty `list` automatically upon the first access of a missing key.
* **Why it's preferred**:
  * **Eliminates redundant checks**: Replaces repetitive manual boilerplate (`if key not in d: d[key] = []`) with `grouped[key].append(item)`.
  * **Performance**: Avoids performing two separate hash lookups (one for `if key not in d` and another for `d[key].append()`), performing the key lookup and list resolution in a single pass in **$\mathcal{O}(1)$ average time** per item (**$\mathcal{O}(n)$ total** for $n$ records).
