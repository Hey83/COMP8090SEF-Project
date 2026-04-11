"""
heapsort - in-place O(n log n) sorting algorithm.

algorithm steps:
  phase 1 - build max-heap: heapify all internal nodes bottom-up in O(n).
  phase 2 - sort: repeatedly swap root (max) with the last unsorted element
             then sift down to restore the heap, shrinking the heap by 1.

time complexity  : O(n log n) - both average and worst case
space complexity : O(1) - in-place, no extra memory beyond the input array
not stable       : equal elements may change relative order
"""


def heapsort(arr):
    """sort arr in-place ascending; returns arr for convenience"""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)
    return arr


def _sift_down(arr, i, heap_size):
    while True:
        largest, l, r = i, 2 * i + 1, 2 * i + 2
        if l < heap_size and arr[l] > arr[largest]:
            largest = l
        if r < heap_size and arr[r] > arr[largest]:
            largest = r
        if largest == i:
            break
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest
