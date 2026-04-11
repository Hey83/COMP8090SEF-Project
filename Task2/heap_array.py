"""
array-based (tree-based) max-heap.

the binary tree is stored implicitly in a list:
  parent(i)     = (i - 1) // 2
  left_child(i) = 2 * i + 1
  right_child(i)= 2 * i + 2

time complexity:
  insert      : O(log n)
  extract_max : O(log n)
  peek        : O(1)
  from_list   : O(n)  - bottom-up heapify
space: O(n)
"""


class ArrayHeap:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"ArrayHeap({self._data})"

    @classmethod
    def from_list(cls, items):
        """build heap in O(n) using bottom-up heapify"""
        h = cls()
        h._data = list(items)
        for i in range(len(h._data) // 2 - 1, -1, -1):
            h._sift_down(i)
        return h

    def insert(self, key):
        self._data.append(key)
        self._sift_up(len(self._data) - 1)

    def extract_max(self):
        if not self._data:
            raise IndexError("heap is empty")
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        val = self._data.pop()
        if self._data:
            self._sift_down(0)
        return val

    def peek(self):
        if not self._data:
            raise IndexError("heap is empty")
        return self._data[0]

    def _sift_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self._data[i] > self._data[p]:
                self._data[i], self._data[p] = self._data[p], self._data[i]
                i = p
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            largest, l, r = i, 2 * i + 1, 2 * i + 2
            if l < n and self._data[l] > self._data[largest]:
                largest = l
            if r < n and self._data[r] > self._data[largest]:
                largest = r
            if largest == i:
                break
            self._data[i], self._data[largest] = self._data[largest], self._data[i]
            i = largest
