"""
pointer-based max-heap.

each node holds explicit left/right/parent pointers.
the complete binary tree property is maintained by tracking the tree size:
  to reach 1-based index k, strip the leading 1-bit then follow
  remaining bits (0 -> left, 1 -> right) from the root.

time complexity:
  insert      : O(log n)
  extract_max : O(log n)
  peek        : O(1)
space: O(n)
"""


class _Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class PointerHeap:
    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"PointerHeap(size={self._size}, max={self._root.key if self._root else None})"

    def insert(self, key):
        node = _Node(key)
        self._size += 1
        if self._size == 1:
            self._root = node
            return
        parent = self._node_at(self._size >> 1)
        node.parent = parent
        if self._size & 1:
            parent.right = node
        else:
            parent.left = node
        self._bubble_up(node)

    def extract_max(self):
        if self._root is None:
            raise IndexError("heap is empty")
        val = self._root.key
        if self._size == 1:
            self._root = None
            self._size = 0
            return val
        last = self._node_at(self._size)
        self._root.key = last.key
        if last.parent.right is last:
            last.parent.right = None
        else:
            last.parent.left = None
        self._size -= 1
        self._sift_down(self._root)
        return val

    def peek(self):
        if self._root is None:
            raise IndexError("heap is empty")
        return self._root.key

    def _node_at(self, index):
        """navigate to the node at 1-based index using bit decomposition"""
        bits = []
        i = index
        while i > 1:
            bits.append(i & 1)
            i >>= 1
        node = self._root
        for bit in reversed(bits):
            node = node.right if bit else node.left
        return node

    def _bubble_up(self, node):
        while node.parent and node.key > node.parent.key:
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent

    def _sift_down(self, node):
        while True:
            largest = node
            if node.left and node.left.key > largest.key:
                largest = node.left
            if node.right and node.right.key > largest.key:
                largest = node.right
            if largest is node:
                break
            node.key, largest.key = largest.key, node.key
            node = largest
