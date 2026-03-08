# heap.py

from ast import Return
from operator import index


class MinHeap:
    
    def __init__(self):
        # Heap starts empty; index 0 is dummy
        self.heap = [None]
        
    def _parent(self, i):
        # Return index of parent of node at index i
        return i // 2
    
    def _left(self, i):
        # Return index of left child of node at index i
        return 2 * i
    
    def _right(self, i):
        # Return index of right child of node at index i
        return 2 * i + 1
    
    def _sift_up(self, i):
        # Move the element at index i up to restore heap property
        while i > 1 and self.heap[i] < self.heap[self._parent(i)]:
            # Swap with parent
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)
    
    def _sift_down(self, i):
        # Move the element at index i down to restore heap property 
        size = len(self.heap) - 1 
        
        while True:
            smallest = i
            left = self._left(i)
            right = self._right(i)
            
            if left <= size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right <= size and self.heap[right] < self.heap[smallest]:
                smallest = right
                
            if smallest == i:
                break
                
            # Swap with smallest child
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest
    
    def __str__(self):
        return str(self.heap[1:])
