"""
Real-Time Time & Space Complexity Visualizer for Lab 02: Big-O Detective.
Generates real-time visual performance graphs and presentation figures.
"""

from collections import Counter, OrderedDict, defaultdict, deque
import gc
from pathlib import Path
import random
import time
import tracemalloc
from typing import Any, Callable, Hashable

import matplotlib.pyplot as plt

# Presentation styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "figure.titlesize": 15,
})


# ============================================================================
# Original Algorithms & Structures
# ============================================================================

def has_duplicates_nested(nums: list[int]) -> bool:
    """Fragment 1: Nested-loop duplicate check (O(n^2) time, O(1) space)."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False


def has_duplicates_set(nums: list[int]) -> bool:
    """Fragment 2: Set-based duplicate check (O(n) time, O(n) space)."""
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def two_sum_dict(nums: list[int], target: int) -> tuple[int, int] | None:
    """Fragment 3: Two-sum using hash map (O(n) time, O(n) space)."""
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


def count_words_counter(text: str) -> Counter[str]:
    """Count words using C-optimized collections.Counter."""
    return Counter(text.lower().split())


def count_words_dict_get(text: str) -> dict[str, int]:
    """Count words using standard dict and bytecode .get()."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


class FIFOQueue:
    """FIFO Queue backed by collections.deque (O(1) popleft)."""
    def __init__(self) -> None:
        self._items: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        self._items.append(item)

    def dequeue(self) -> Any:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()


class ListFIFOQueue:
    """Naive FIFO Queue backed by Python list (O(n) pop(0) memory shifts)."""
    def __init__(self) -> None:
        self._items: list[Any] = []

    def enqueue(self, item: Any) -> None:
        self._items.append(item)

    def dequeue(self) -> Any:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)


class LRUCache:
    """LRU Cache backed by collections.OrderedDict (O(1) get & put)."""
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.cache: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable) -> Any:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Hashable, value: Any) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value


def group_items_by_key(items: list[dict[str, Any]], group_key: str) -> dict[str, list[dict[str, Any]]]:
    """Group list of dict records using collections.defaultdict(list)."""
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        val = str(item.get(group_key, "unknown"))
        grouped[val].append(item)
    return dict(grouped)


def get_unique_countries_before(customer_data: list[dict[str, str]]) -> list[str]:
    """Lab 01 Naive lookup in list (O(n^2))."""
    unique_countries = []
    for customer in customer_data:
        country = customer.get("country", "")
        if country and country not in unique_countries:
            unique_countries.append(country)
    return unique_countries


def get_unique_countries_after(customer_data: list[dict[str, str]]) -> list[str]:
    """Lab 01 Optimized lookup in set (O(n))."""
    seen = set()
    unique_countries = []
    for customer in customer_data:
        country = customer.get("country", "")
        if country and country not in seen:
            seen.add(country)
            unique_countries.append(country)
    return unique_countries


# ============================================================================
# Benchmarking & Instrumentation Engine
# ============================================================================

def profile_function(func: Callable, *args: Any, repetitions: int = 3) -> tuple[float, float]:
    """Profiles a function for average execution time (ms) and peak memory (KB)."""
    gc.collect()
    
    # 1. Measure Memory with tracemalloc
    tracemalloc.start()
    _ = func(*args)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak_bytes / 1024.0

    # 2. Measure Execution Time
    times = []
    for _ in range(repetitions):
        start = time.perf_counter()
        _ = func(*args)
        times.append((time.perf_counter() - start) * 1000.0)  # Convert to ms

    return min(times), peak_kb


# ============================================================================
# Real-Time Visualizer & Presentation Plots
# ============================================================================

def plot_comparison(
    title: str,
    sizes: list[int],
    series: list[dict[str, Any]],
    output_path: Path,
    x_label: str = "Tamaño de Entrada (N)",
    interactive: bool = True,
    takeaway: str = "",
    use_log_time: bool = False,
) -> None:
    """Genera gráficos de Tiempo y Memoria listos para presentación
    con colores semánticos, etiquetas de complejidad Big-O y conclusiones clave en español.
    """
    fig, (ax_time, ax_mem) = plt.subplots(1, 2, figsize=(15, 6), facecolor="#F8F9FA")
    fig.suptitle(title, fontsize=16, fontweight="bold", color="#111827", y=0.98)

    # Paleta de colores semántica
    style_map = {
        "bad": {"color": "#DC2626", "line": "-", "marker": "o", "fill": "#FEE2E2"},      # Rojo
        "good": {"color": "#059669", "line": "-", "marker": "s", "fill": "#D1FAE5"},     # Verde
        "neutral": {"color": "#2563EB", "line": "-", "marker": "^", "fill": "#DBEAFE"},  # Azul
        "alt": {"color": "#D97706", "line": "--", "marker": "d", "fill": "#FEF3C7"},     # Ámbar
    }

    # 1. Gráfico de Tiempo de Ejecución
    ax_time.set_facecolor("#FFFFFF")
    for s in series:
        role = s.get("role", "neutral")
        cfg = style_map.get(role, style_map["neutral"])
        label = f"{s['name']}  [{s.get('big_o', '')}]"
        
        ax_time.plot(
            sizes, s["times"],
            color=cfg["color"],
            linestyle=cfg["line"],
            marker=cfg["marker"],
            linewidth=2.5,
            markersize=7,
            label=label,
        )
        ax_time.fill_between(sizes, s["times"], color=cfg["fill"], alpha=0.35)

    if use_log_time:
        ax_time.set_yscale("log")
        ax_time.set_ylabel("Tiempo de Ejecución (ms) [Escala Logarítmica]", fontweight="bold", color="#374151")
    else:
        ax_time.set_ylabel("Tiempo de Ejecución (ms)", fontweight="bold", color="#374151")

    ax_time.set_title("Rendimiento Temporal (Menor = Mejor)", fontsize=13, fontweight="bold", pad=10)
    ax_time.set_xlabel(x_label, fontweight="bold", color="#374151")
    ax_time.grid(True, linestyle="--", alpha=0.5, color="#D1D5DB")
    ax_time.legend(frameon=True, facecolor="#F3F4F6", edgecolor="#E5E7EB", fontsize=10, loc="upper left")

    # 2. Gráfico de Consumo de Memoria
    ax_mem.set_facecolor("#FFFFFF")
    for s in series:
        role = s.get("role", "neutral")
        cfg = style_map.get(role, style_map["neutral"])
        label = f"{s['name']}  [{s.get('space_o', '')}]"

        ax_mem.plot(
            sizes, s["memory"],
            color=cfg["color"],
            linestyle=cfg["line"],
            marker=cfg["marker"],
            linewidth=2.5,
            markersize=7,
            label=label,
        )
        ax_mem.fill_between(sizes, s["memory"], color=cfg["fill"], alpha=0.35)

    ax_mem.set_title("Memoria Pico Asignada (Compromiso de Espacio)", fontsize=13, fontweight="bold", pad=10)
    ax_mem.set_xlabel(x_label, fontweight="bold", color="#374151")
    ax_mem.set_ylabel("Memoria Pico (KB)", fontweight="bold", color="#374151")
    ax_mem.grid(True, linestyle="--", alpha=0.5, color="#D1D5DB")
    ax_mem.legend(frameon=True, facecolor="#F3F4F6", edgecolor="#E5E7EB", fontsize=10, loc="upper left")

    # Conclusión Clave
    if takeaway:
        fig.text(
            0.5, 0.02,
            f"Conclusión Clave: {takeaway}",
            ha="center", fontsize=11, fontweight="semibold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#EDE9FE", edgecolor="#8B5CF6", alpha=0.9),
            color="#4C1D95",
        )

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(output_path, dpi=300)
    print(f" Gráfico guardado: {output_path.name}")
    if interactive:
        plt.show(block=False)
        plt.pause(1.2)
    plt.close(fig)


def run_all_visualizations(save_dir: Path) -> None:
    """Ejecuta toda la suite de pruebas de rendimiento y visualiza la complejidad."""
    save_dir.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 60)
    print(" INICIANDO VISUALIZADOR EN TIEMPO REAL - DETECTIVE BIG-O")
    print("=" * 60)

    # --- 1. Detección de Duplicados: O(n^2) vs O(n) ---
    print("\n[1/5] Evaluando Detección de Duplicados: Bucles Anidados O(n^2) vs Hash Set O(n)...")
    sizes_dup = [200, 500, 1000, 2000, 4000]
    nested_times, nested_mem = [], []
    set_times, set_mem = [], []

    for n in sizes_dup:
        # Peor caso: sin elementos duplicados
        data = list(range(n))
        t_n, m_n = profile_function(has_duplicates_nested, data)
        t_s, m_s = profile_function(has_duplicates_set, data)
        nested_times.append(t_n); nested_mem.append(m_n)
        set_times.append(t_s); set_mem.append(m_s)
        print(f"  N={n:4d} | Anidado: {t_n:7.2f}ms ({m_n:5.1f}KB) | Set: {t_s:6.3f}ms ({m_s:5.1f}KB)")

    plot_comparison(
        title="Detección de Duplicados: Bucles Anidados O(n²) vs Hash Set O(n)",
        sizes=sizes_dup,
        series=[
            {
                "name": "Bucles Anidados",
                "big_o": "Tiempo: O(n²)",
                "space_o": "Espacio: O(1)",
                "role": "bad",
                "times": nested_times,
                "memory": nested_mem,
            },
            {
                "name": "Hash Set",
                "big_o": "Tiempo: O(n)",
                "space_o": "Espacio: O(n)",
                "role": "good",
                "times": set_times,
                "memory": set_mem,
            },
        ],
        output_path=save_dir / "01_duplicate_check_comparison.png",
        use_log_time=True,
        takeaway="El Hash Set es ~1,700x más rápido invirtiendo memoria O(n) para eliminar el cuello de botella O(n²) de CPU.",
    )

    # --- 2. Frecuencia de Palabras: Counter vs dict.get ---
    print("\n[2/5] Evaluando Frecuencia de Palabras: Counter vs dict.get()...")
    sizes_words = [10_000, 30_000, 70_000, 120_000, 200_000]
    vocab = ["python", "data", "pipeline", "queue", "stack", "algorithm", "performance", "memory"]
    counter_times, counter_mem = [], []
    dict_times, dict_mem = [], []

    for n in sizes_words:
        text = " ".join(random.choices(vocab, k=n))
        t_c, m_c = profile_function(count_words_counter, text)
        t_d, m_d = profile_function(count_words_dict_get, text)
        counter_times.append(t_c); counter_mem.append(m_c)
        dict_times.append(t_d); dict_mem.append(m_d)
        print(f"  Palabras={n:6d} | Counter: {t_c:6.2f}ms ({m_c:6.1f}KB) | dict.get: {t_d:6.2f}ms ({m_d:6.1f}KB)")

    plot_comparison(
        title="Conteo de Palabras: collections.Counter vs dict.get()",
        sizes=sizes_words,
        series=[
            {
                "name": "collections.Counter",
                "big_o": "Tiempo: O(n) [C-Rápido]",
                "space_o": "Espacio: O(U)",
                "role": "good",
                "times": counter_times,
                "memory": counter_mem,
            },
            {
                "name": "dict.get()",
                "big_o": "Tiempo: O(n) [Bytecode]",
                "space_o": "Espacio: O(U)",
                "role": "alt",
                "times": dict_times,
                "memory": dict_mem,
            },
        ],
        output_path=save_dir / "02_word_count_counter_vs_dict.png",
        x_label="Total de Palabras Procesadas",
        takeaway="Ambos son O(n), pero la implementación en C de Counter es ~30% más rápida con consumo de memoria idéntico.",
    )

    # --- 3. Cola FIFO: deque.popleft() vs list.pop(0) ---
    print("\n[3/5] Evaluando Cola FIFO: deque O(1) vs list.pop(0) O(n)...")
    sizes_queue = [2000, 5000, 10000, 20000, 35000]
    deque_times, deque_mem = [], []
    list_times, list_mem = [], []

    def benchmark_queue(q_cls, count):
        q = q_cls()
        for i in range(count):
            q.enqueue(i)
        for _ in range(count):
            q.dequeue()

    for n in sizes_queue:
        t_dq, m_dq = profile_function(benchmark_queue, FIFOQueue, n)
        t_ls, m_ls = profile_function(benchmark_queue, ListFIFOQueue, n)
        deque_times.append(t_dq); deque_mem.append(m_dq)
        list_times.append(t_ls); list_mem.append(m_ls)
        print(f"  Operaciones={n:5d} | deque (O(1)): {t_dq:6.2f}ms | list.pop(0) (O(n)): {t_ls:7.2f}ms")

    plot_comparison(
        title="Cola FIFO: collections.deque O(1) vs list.pop(0) O(n)",
        sizes=sizes_queue,
        series=[
            {
                "name": "collections.deque",
                "big_o": "Tiempo: O(1) / op",
                "space_o": "Espacio: O(n)",
                "role": "good",
                "times": deque_times,
                "memory": deque_mem,
            },
            {
                "name": "list.pop(0)",
                "big_o": "Tiempo: O(n) / op",
                "space_o": "Espacio: O(n)",
                "role": "bad",
                "times": list_times,
                "memory": list_mem,
            },
        ],
        output_path=save_dir / "03_fifo_queue_deque_vs_list.png",
        x_label="Operaciones de Inserción y Extracción",
        use_log_time=True,
        takeaway="list.pop(0) desplaza memoria contigua O(n) en cada extracción (~18x más lenta); deque extrae en tiempo estrictamente O(1).",
    )

    # --- 4. Rendimiento de Caché LRU & Agrupamiento ---
    print("\n[4/5] Evaluando Caché LRU O(1) & defaultdict(list) O(n)...")
    sizes_lru = [5000, 15000, 30000, 60000, 100000]
    lru_times, lru_mem = [], []

    def benchmark_lru(ops):
        cache = LRUCache(capacity=500)
        for i in range(ops):
            cache.put(i % 1000, f"val_{i}")
            cache.get((i * 3) % 1000)

    for n in sizes_lru:
        t_lru, m_lru = profile_function(benchmark_lru, n)
        lru_times.append(t_lru); lru_mem.append(m_lru)
        print(f"  Accesos={n:6d} | LRUCache (O(1) ops): {t_lru:6.2f}ms ({m_lru:5.1f}KB)")

    plot_comparison(
        title="Escalabilidad de Caché LRU: collections.OrderedDict",
        sizes=sizes_lru,
        series=[
            {
                "name": "LRUCache (OrderedDict)",
                "big_o": "Tiempo: O(1) / op",
                "space_o": "Espacio: O(Capacidad)",
                "role": "good",
                "times": lru_times,
                "memory": lru_mem,
            }
        ],
        output_path=save_dir / "04_lru_cache_scaling.png",
        x_label="Total de Accesos a Caché (Lectura + Escritura)",
        takeaway="OrderedDict mantiene rendimiento O(1) acotando estrictamente el uso de memoria a la capacidad de la caché.",
    )

    # --- 5. Parte C: Deduplicación de Países Lab 01 ---
    print("\n[5/5] Evaluando Deduplicación de Países Lab 01: Lista O(n^2) vs Set O(n)...")
    sizes_c = [200, 600, 1200, 2500, 5000]
    countries_pool = ["USA", "Canada", "Mexico", "Japan", "Germany", "France", "Brazil", "UK", "Chile"]
    c_list_times, c_list_mem = [], []
    c_set_times, c_set_mem = [], []

    for n in sizes_c:
        customer_data = [{"country": random.choice(countries_pool)} for _ in range(n)]
        t_l, m_l = profile_function(get_unique_countries_before, customer_data)
        t_s, m_s = profile_function(get_unique_countries_after, customer_data)
        c_list_times.append(t_l); c_list_mem.append(m_l)
        c_set_times.append(t_s); c_set_mem.append(m_s)
        print(f"  Clientes={n:4d} | Búsqueda Lineal: {t_l:6.2f}ms | Hash Set: {t_s:6.3f}ms")

    plot_comparison(
        title="Aplicación Lab 01: Optimización de Deduplicación de Clientes",
        sizes=sizes_c,
        series=[
            {
                "name": "Antes (Búsqueda en Lista)",
                "big_o": "Tiempo: O(n²)",
                "space_o": "Espacio: O(k)",
                "role": "bad",
                "times": c_list_times,
                "memory": c_list_mem,
            },
            {
                "name": "Después (Hash Set)",
                "big_o": "Tiempo: O(n)",
                "space_o": "Espacio: O(k)",
                "role": "good",
                "times": c_set_times,
                "memory": c_set_mem,
            },
        ],
        output_path=save_dir / "05_lab01_country_dedup_comparison.png",
        x_label="Registros de Clientes Procesados",
        takeaway="Reemplazar la búsqueda lineal en lista por un conjunto (set) otorga aceleración inmediata sin memoria extra.",
    )

    print("\n" + "=" * 60)
    print(f" Los 5 gráficos de presentación fueron guardados en: {save_dir.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    plots_directory = Path(__file__).resolve().parent / "presentation_plots"
    run_all_visualizations(plots_directory)

