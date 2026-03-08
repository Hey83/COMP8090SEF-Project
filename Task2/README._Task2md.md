# Self-Study on Heap Data Structure and Heap Sort Algorithm

## Overview

### 1. Binary Heap (Data Structure)
- **Abstract Data Type (ADT)**: Priority Queue (supports efficient insert and extract-min/max operations)
- **Type**: Min-Heap (can be easily adapted to Max-Heap)
- **Representation**: Array-based complete binary tree
- **Main Operations**:
  - `insert(value)` → O(log n)
  - `extract_min()` → O(log n)
  - `heapify()` (bottom-up) → O(n) for building heap
  - `peek()` / `get_min()` → O(1)

### 2. Heap Sort (Algorithm)
- **Type**: Comparison-based, in-place sorting algorithm
- **Time Complexity**:
  - Worst/Average/Best: **O(n log n)**
  - Build heap phase: **O(n)**
  - Extraction phase: **O(n log n)**
- **Space Complexity**: **O(1)**
- **Stability**: Not stable
- **Advantages**: Guaranteed O(n log n), in-place, good cache performance in practice
- **Disadvantages**: Not adaptive (always O(n log n) even if nearly sorted), slower than quicksort in average case due to poor locality

## Files in this folder (/task2 or root)

- `heap.py`          → Binary Min-Heap class implementation
- `heapsort.py`      → Heap Sort function using the heap implementation
- `demo.py`          → Simple demonstration and test cases

## How to Run (User Guide)

Requires **Python 3.8+**
