"""
heap data structure & heapsort - self-study demo.

heap ADT
--------
a heap is a complete binary tree satisfying the heap property:
  max-heap: every node >= its children  (root holds the maximum)
  min-heap: every node <= its children

two representations:
  array-based  - store tree levels left-to-right in a list; O(1) index arithmetic
  pointer-based - explicit left/right/parent pointers; mirrors a linked-list tree
"""

from heap_array import ArrayHeap
from heap_pointer import PointerHeap
from heapsort import heapsort
import benchmark


def demo_array_heap():
    print("array-based heap")
    h = ArrayHeap()
    values = [5, 3, 8, 1, 9, 2, 7]
    for v in values:
        h.insert(v)
    print(f"  inserted: {values}")
    print(f"  max: {h.peek()}")
    out = []
    while len(h):
        out.append(h.extract_max())
    print(f"  extract_max: {out}")


def demo_pointer_heap():
    print("\npointer-based heap")
    h = PointerHeap()
    values = [4, 10, 3, 5, 1, 8, 6]
    for v in values:
        h.insert(v)
    print(f"  inserted: {values}")
    print(f"  max: {h.peek()}")
    out = []
    while len(h):
        out.append(h.extract_max())
    print(f"  extract_max: {out}")


def demo_heapsort():
    from heapsort import _sift_down
    print("\nheapsort")
    data = [64, 25, 12, 22, 11]
    arr = list(data)
    n = len(arr)
    print(f"  input: {arr}")
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)
    print(f"  after heapify: {arr}")
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)
        print(f"  step {n - end}: {arr}")
    print(f"  result: {heapsort(list(data))}")


def main():
    demo_array_heap()
    demo_pointer_heap()
    demo_heapsort()
    print()
    benchmark.run()


if __name__ == "__main__":
    main()
