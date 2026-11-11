"""Unit test suite for all 6 classic algorithms using pytest.

Week 6: Algorithms & Building APIs - Lab 06
"""

import pytest
from algorithms.linked_lists import LinkedList
from algorithms.lru_cache import LRUCache
from algorithms.char_hash import first_non_repeating_char
from algorithms.graph_cycle import has_cycle
from algorithms.merge_intervals import merge_intervals
from algorithms.binary_search import integer_sqrt


# ==========================================
# 1. Test: Inversión de Lista Enlazada
# ==========================================
def test_reverse_linked_list():
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)

    ll.reverse()
    assert ll.to_list() == [5, 4, 3, 2, 1]


def test_reverse_empty_and_single_node_linked_list():
    empty_ll = LinkedList()
    empty_ll.reverse()
    assert empty_ll.to_list() == []

    single_ll = LinkedList()
    single_ll.append(42)
    single_ll.reverse()
    assert single_ll.to_list() == [42]


# ==========================================
# 2. Test: Caché LRU
# ==========================================
def test_lru_cache_eviction_and_access():
    cache = LRUCache(capacity=2)
    cache.put(1, 100)
    cache.put(2, 200)

    # Acceder a 1 lo vuelve el más recientemente usado
    assert cache.get(1) == 100

    # Insertar 3 debe evacuar la clave 2 (Least Recently Used)
    cache.put(3, 300)
    assert cache.get(2) == -1
    assert cache.get(3) == 300
    assert cache.get(1) == 100


def test_lru_cache_update_existing_key():
    cache = LRUCache(capacity=2)
    cache.put(1, 100)
    cache.put(2, 200)
    cache.put(1, 150)  # Actualizar clave 1

    cache.put(3, 300)  # Debe evacuar 2, no 1
    assert cache.get(1) == 150
    assert cache.get(2) == -1
    assert cache.get(3) == 300


# ==========================================
# 3. Test: Primer Carácter No Repetido
# ==========================================
def test_first_non_repeating_char():
    assert first_non_repeating_char("leetcode") == 0      # 'l'
    assert first_non_repeating_char("loveleetcode") == 2  # 'v'
    assert first_non_repeating_char("aabb") == -1         # Sin caracteres únicos


# ==========================================
# 4. Test: Detección de Ciclos en Grafos
# ==========================================
def test_graph_cycle_detection():
    cyclic_graph = {0: [1], 1: [2], 2: [0]}
    acyclic_graph = {0: [1], 1: [2], 2: []}
    disconnected_cyclic = {0: [1], 1: [], 2: [3], 3: [2]}

    assert has_cycle(cyclic_graph) is True
    assert has_cycle(acyclic_graph) is False
    assert has_cycle(disconnected_cyclic) is True


def test_graph_self_loop():
    self_loop = {0: [0]}
    assert has_cycle(self_loop) is True


# ==========================================
# 5. Test: Fusión de Intervalos
# ==========================================
def test_merge_intervals():
    raw_intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    expected = [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals(raw_intervals) == expected


def test_merge_intervals_unordered_and_nested():
    unordered = [[1, 4], [4, 5], [0, 2]]
    expected = [[0, 5]]
    assert merge_intervals(unordered) == expected

    empty = []
    assert merge_intervals(empty) == []


# ==========================================
# 6. Test: Raíz Cuadrada Entera (Binary Search)
# ==========================================
def test_integer_sqrt():
    assert integer_sqrt(4) == 2
    assert integer_sqrt(8) == 2   # floor(sqrt(8)) = 2
    assert integer_sqrt(16) == 4
    assert integer_sqrt(0) == 0
    assert integer_sqrt(1) == 1


def test_integer_sqrt_negative_value():
    with pytest.raises(ValueError):
        integer_sqrt(-5)
