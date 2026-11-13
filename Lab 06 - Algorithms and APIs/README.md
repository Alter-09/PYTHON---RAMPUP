# Lab 06: Algorithms & Building APIs

A complete, tested Python project containing solutions to 6 classic computer science algorithmic challenges alongside a robust, fully validated REST API built with **FastAPI** and **Pydantic**.

---

## Project Structure

```text
Lab 06 - Algorithms and APIs/
├── algorithms/
│   ├── __init__.py
│   ├── binary_search.py        # Integer square root using binary search
│   ├── char_hash.py            # First non-repeating character in string
│   ├── graph_cycle.py          # Directed graph cycle detection (DFS + visited set)
│   ├── linked_lists.py         # Singly linked list & iterative reversal
│   ├── lru_cache.py            # O(1) LRU Cache using OrderedDict
│   ├── merge_intervals.py      # Overlapping intervals merge
│   └── test_algorithms.py      # Comprehensive pytest suite for algorithms
├── bookstore/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application with CRUD endpoints
│   ├── models.py               # Pydantic Book model with custom validators
│   └── test_api.py             # FastAPI TestClient test suite
└── README.md                   # Lab documentation, execution guide & reflection
```

---

## 1. Algorithm Complexity & Design Notes

Each algorithm is implemented with explicit complexity guarantees and clean docstrings:

| Problem | Module | Time Complexity | Space Complexity | Algorithmic Strategy & Reasoning |
| :--- | :--- | :---: | :---: | :--- |
| **Reverse Linked List** | `linked_lists.py` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Single linear pass through the list using 3 pointers (`prev`, `current`, `next_node`) rewiring link directions in-place with zero heap allocations. |
| **LRU Cache** | `lru_cache.py` | $\mathcal{O}(1)$ | $\mathcal{O}(C)$ | Leverages `collections.OrderedDict`, combining a hash table for key lookups with an underlying doubly linked list. Key accesses invoke `move_to_end()` in $\mathcal{O}(1)$, and overflow triggers `popitem(last=False)` in $\mathcal{O}(1)$. $C$ represents fixed capacity. |
| **First Non-Repeating Char** | `char_hash.py` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Two-pass approach: first pass counts frequency using `collections.Counter` ($\mathcal{O}(n)$ time), second pass scans the string to return the first index with count $1$. Space is $\mathcal{O}(1)$ because the character hash map is strictly bounded by the fixed alphabet size ($\le 26$). |
| **Graph Cycle Detection** | `graph_cycle.py` | $\mathcal{O}(V + E)$ | $\mathcal{O}(V)$ | Depth-First Search (DFS) utilizing two tracking sets: `visited` tracks permanently processed vertices, while `rec_stack` tracks vertices currently in the recursion stack. A back-edge to an element in `rec_stack` immediately confirms a cycle. |
| **Merge Intervals** | `merge_intervals.py` | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Intervals are sorted by start value $\mathcal{O}(n \log n)$. A single linear scan consolidates overlapping ranges if $start_{curr} \le end_{prev}$ by updating $end_{prev} = \max(end_{prev}, end_{curr})$, appending non-overlapping ranges directly. |
| **Integer Square Root** | `binary_search.py` | $\mathcal{O}(\log x)$ | $\mathcal{O}(1)$ | Binary search over the candidate range $[1, \lfloor x / 2 \rfloor]$. Halves the search space at each iteration to find $\lfloor \sqrt{x} \rfloor$ without utilizing floating-point arithmetic or external dependencies. |

---

## 2. Bookstore REST API (FastAPI)

The API provides in-memory CRUD operations for books with strict Pydantic data validation.

### Data Model (`Book`)
- **`id`** (`int`): Unique identifier.
- **`title`** (`str`): Title with `min_length=1`.
- **`author`** (`str`): Author name with `min_length=1`.
- **`year`** (`int`): Publication year constrained to $1450 \le \text{year} \le 2026$ (from Gutenberg press era to current year).
- **`isbn`** (`str`): Cleaned 10 or 13 alphanumeric character standard format.

### Endpoints & Exact HTTP Status Codes
- `GET /books` — Returns `200 OK` (supports optional author filter via `?author=name`).
- `GET /books/{id}` — Returns `200 OK` on success, or `404 Not Found` if missing.
- `POST /books` — Returns `201 Created` on valid book, `400 Bad Request` if ID already exists, or `422 Unprocessable Entity` on schema/validation violations.
- `DELETE /books/{id}` — Returns `204 No Content` on successful deletion, or `404 Not Found` if the book does not exist.

---

## 3. How to Run the Tests

Ensure dependencies are installed:
```bash
pip install fastapi uvicorn pydantic pytest httpx
```

### Run the entire test suite (Algorithms + API):
From the root workspace directory:
```bash
pytest "Lab 06 - Algorithms and APIs" -v
```

### Run tests per module:
```bash
# Run algorithms unit tests (11 assertions)
pytest "Lab 06 - Algorithms and APIs/algorithms/test_algorithms.py" -v

# Run Bookstore API client tests
pytest "Lab 06 - Algorithms and APIs/bookstore/test_api.py" -v
```

---

## 4. How to Launch the API Server (`uvicorn`)

To start the local development server with hot-reload enabled:

```bash
uvicorn bookstore.main:app --reload --host 127.0.0.1 --port 8000 --app-dir "Lab 06 - Algorithms and APIs"
```

Once running, interactive documentation is automatically available:
- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Alternative**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 5. Architectural Reflection: REST vs. GraphQL for this Bookstore API

### When REST is the Right Choice (Current Implementation)
1. **Simplicity and Predictability**:
   - For resource-oriented entities with straightforward CRUD semantics (`Book`), REST maps cleanly onto standard HTTP verbs (`GET`, `POST`, `DELETE`) and standard HTTP status codes (`200`, `201`, `204`, `404`, `422`).
2. **Native HTTP Caching & Edge CDNs**:
   - GET endpoints such as `/books/{id}` or `/books` can be natively cached by CDNs, reverse proxies, and browsers based on HTTP caching headers (`Cache-Control`, `ETag`). In GraphQL, because all requests typically go to a single `/graphql` POST endpoint, caching requires specialized client libraries (e.g., Apollo Client normalization) or complex persisted queries.
3. **Low Complexity & Zero Overhead**:
   - REST endpoints are lightweight to build, maintain, and secure (no AST query parsing, no execution plan overhead, and no risk of malicious deeply-nested recursive queries).

### When GraphQL Would Be Superior
1. **Over-fetching & Under-fetching Prevention**:
   - If a mobile client only requires the book title and author to render a list view (e.g. `query { books { title author } }`), REST forces the server to transfer the full payload (`id`, `isbn`, `year`, and potential future metadata like summaries, reviews, and high-res cover links). GraphQL eliminates this bandwidth waste.
2. **Relational & Nested Queries**:
   - If the domain expands to include `authors`, `reviews`, `genres`, and `publishers`, fetching a book and its top 3 reviews in REST typically leads to the $N+1$ request problem (fetching `/books/{id}` followed by multiple requests to `/books/{id}/reviews`). With GraphQL, the client requests everything in a single round-trip:
     ```graphql
     query {
       book(id: 101) {
         title
         reviews(limit: 3) {
           rating
           comment
         }
       }
     }
     ```
3. **Decoupled Client Evolution**:
   - Different frontend platforms (web, mobile, smart readers) can request distinct shapes of data without requiring backend engineers to create new custom REST endpoints or expand query parameters.

### Conclusion for This Bookstore Service
For the current scope (simple in-memory CRUD operations over a single entity), **REST with FastAPI is the superior architectural choice**. It provides optimal developer velocity, zero query parsing overhead, native HTTP status semantics, and automatic OpenAPI documentation. GraphQL would become justified if the bookstore evolved into a multi-entity relational platform with diverse frontend client bandwidth constraints.

