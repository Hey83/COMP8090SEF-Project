"""
benchmarks heap insert/extract and heapsort against built-in alternatives.
produces a 3-panel plot saved to benchmark.png.
"""

import random
import time

import matplotlib.pyplot as plt

from heap_array import ArrayHeap
from heap_pointer import PointerHeap
from heapsort import heapsort

SIZES = [1000, 5000, 10000, 50000, 100000, 200000]
RUNS = 3


def _mean_time(fn, *args) -> float:
    times = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - t0)
    return sum(times) / RUNS


def bench_insert(sizes):
    array_times, pointer_times = [], []
    for n in sizes:
        data = [random.randint(0, n * 10) for _ in range(n)]

        def do_array():
            h = ArrayHeap()
            for x in data:
                h.insert(x)

        def do_pointer():
            h = PointerHeap()
            for x in data:
                h.insert(x)

        array_times.append(_mean_time(do_array))
        pointer_times.append(_mean_time(do_pointer))
    return array_times, pointer_times


def bench_extract(sizes):
    array_times, pointer_times = [], []
    for n in sizes:
        data = [random.randint(0, n * 10) for _ in range(n)]

        def do_array(d=data):
            h = ArrayHeap.from_list(d)
            while len(h):
                h.extract_max()

        def do_pointer(d=data):
            h = PointerHeap()
            for x in d:
                h.insert(x)
            while len(h):
                h.extract_max()

        array_times.append(_mean_time(do_array))
        pointer_times.append(_mean_time(do_pointer))
    return array_times, pointer_times


def bench_sort(sizes):
    heap_times, builtin_times = [], []
    for n in sizes:
        data = [random.randint(0, n * 10) for _ in range(n)]

        heap_times.append(_mean_time(lambda d=data: heapsort(list(d))))
        builtin_times.append(_mean_time(lambda d=data: sorted(d)))
    return heap_times, builtin_times


def bench_heapify(sizes):
    """O(n) from_list (bottom-up) vs O(n log n) repeated insert"""
    heapify_times, insert_times = [], []
    for n in sizes:
        data = [random.randint(0, n * 10) for _ in range(n)]

        heapify_times.append(_mean_time(lambda d=data: ArrayHeap.from_list(d)))

        def do_insert(d=data):
            h = ArrayHeap()
            for x in d:
                h.insert(x)

        insert_times.append(_mean_time(do_insert))
    return heapify_times, insert_times


def run():
    random.seed(42)
    print("benchmarking - this may take a moment ...")

    insert_arr, insert_ptr = bench_insert(SIZES)
    extract_arr, extract_ptr = bench_extract(SIZES)
    sort_heap, sort_builtin = bench_sort(SIZES)
    heapify_fast, heapify_slow = bench_heapify(SIZES)

    _print_table("insert (s)", SIZES, insert_arr, insert_ptr, "array", "pointer")
    _print_table("extract_max (s)", SIZES, extract_arr, extract_ptr, "array", "pointer")
    _print_table("sort (s)", SIZES, sort_heap, sort_builtin, "heapsort", "sorted()")
    _print_table("heapify (s)", SIZES, heapify_fast, heapify_slow, "from_list O(n)", "n*insert O(nlogn)")

    _plot(SIZES, insert_arr, insert_ptr, extract_arr, extract_ptr,
          sort_heap, sort_builtin, heapify_fast, heapify_slow)


def _print_table(title, sizes, a, b, label_a, label_b):
    print(f"\n{title}")
    print(f"{'n':>6}  {label_a:>12}  {label_b:>12}")
    for n, ta, tb in zip(sizes, a, b):
        print(f"{n:>6}  {ta:>12.6f}  {tb:>12.6f}")


def _plot(sizes, ins_a, ins_p, ext_a, ext_p, srt_h, srt_b, hfy_fast, hfy_slow):
    import numpy as np

    ns = np.array(sizes, dtype=float)
    ms = ns / 1000

    def fit_nlogn(measured):
        theory = ns * np.log2(ns)
        scale = np.mean(np.array(measured) / theory) * 1000
        return theory * scale

    def fit_n(measured):
        scale = np.mean(np.array(measured) / ns) * 1000
        return ns * scale

    def save_fig(filename, title, pairs, ref_curve, ref_label):
        fig, ax = plt.subplots(figsize=(7, 5))
        for values, label, fmt in pairs:
            ax.plot(ms, [t * 1000 for t in values], fmt, label=label)
        ax.plot(ms, ref_curve, "k:", linewidth=1, label=ref_label)
        ax.set_title(title)
        ax.set_xlabel("n (x1000)")
        ax.set_ylabel("time (ms)")
        ax.legend()
        plt.tight_layout()
        plt.savefig(filename, dpi=120)
        plt.close(fig)
        print(f"{filename} saved")

    save_fig("bench_insert.png", "Insert n elements",
             [(ins_a, "ArrayHeap", "o-"), (ins_p, "PointerHeap", "s--")],
             fit_nlogn(ins_a), "O(n log n)")

    save_fig("bench_extract.png", "Extract all elements",
             [(ext_a, "ArrayHeap", "o-"), (ext_p, "PointerHeap", "s--")],
             fit_nlogn(ext_a), "O(n log n)")

    save_fig("bench_sort.png", "Sort n elements",
             [(srt_h, "heapsort", "o-"), (srt_b, "sorted() / timsort", "s--")],
             fit_nlogn(srt_h), "O(n log n)")

    # heapify needs two reference curves so handle separately
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ms, [t * 1000 for t in hfy_fast], "o-", label="from_list  O(n)")
    ax.plot(ms, [t * 1000 for t in hfy_slow], "s--", label="n x insert  O(n log n)")
    ax.plot(ms, fit_n(hfy_fast), "k:", linewidth=1, label="O(n)")
    ax.plot(ms, fit_nlogn(hfy_slow), "k--", linewidth=1, label="O(n log n)")
    ax.set_title("Build heap: from_list vs repeated insert")
    ax.set_xlabel("n (x1000)")
    ax.set_ylabel("time (ms)")
    ax.legend()
    plt.tight_layout()
    plt.savefig("bench_heapify.png", dpi=120)
    plt.close(fig)
    print("bench_heapify.png saved")
