import cProfile
from dataclasses import dataclass
from io import StringIO
import pstats
import time
import tracemalloc
from typing import List

from benchmarks.boards import PRESET_BOARDS
from morajai_solver.core.Solver import MoraSolver
from morajai_solver.models.MoraBoard import DictMoraBoard


@dataclass
class BenchmarkResult:
    name: str
    execution_time_ms: float
    memory_peak_kb: float
    path_length: int
    profile_stats: str


def run_single_bench(name: str, board: DictMoraBoard) -> BenchmarkResult:
    solver = MoraSolver(board)

    tracemalloc.start()

    profiler = cProfile.Profile()
    start_time = time.perf_counter()

    profiler.enable()
    path = solver.solve()
    profiler.disable()

    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time_ms = (end_time - start_time) * 1000

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs().sort_stats("tottime")
    stats.print_stats(8)

    return BenchmarkResult(
        name=name,
        execution_time_ms=execution_time_ms,
        memory_peak_kb=peak_mem / 1024,
        path_length=len(path) if path else 0,
        profile_stats=stream.getvalue(),
    )


def generate_report(results: List[BenchmarkResult]):
    """Génère un affichage propre et lisible dans le terminal."""
    print("\n" + "=" * 72)
    print(" 🚀 BENCHMARK & PROFILAGE CPU — SOLVER MORAJAI")
    print("=" * 72)
    print(
        f"{'Nom de la grille':<35} | {'Temps (ms)':<10} | {'Mém. (KB)':<9} | {'Coups':<5}"
    )
    print("-" * 72)

    total_time = 0.0
    for r in results:
        status_time = f"{r.execution_time_ms:8.2f} ms"
        print(
            f"{r.name:<35} | {status_time:<10} | {r.memory_peak_kb:8.1f} | {r.path_length:<5}"
        )
        total_time += r.execution_time_ms

    print("-" * 72)
    print(f"Temps total cumulé : {total_time:.2f} ms")
    print("=" * 72)

    # Affichage du profil détaillé pour la grille la plus lente
    slowest = max(results, key=lambda x: x.execution_time_ms)
    print("\n🔍 DÉTAILS cProfile (Grille la plus lente : " + slowest.name + ") :")
    print("-" * 72)
    print(slowest.profile_stats)


def main():
    print("Exécution des benchmarks sur les grilles pré-enregistrées...")
    results = [run_single_bench(name, board) for name, board in PRESET_BOARDS]
    generate_report(results)


if __name__ == "__main__":
    main()
