# Dijkstras-Algorithm-for-grid-paths

Dijkstra & Graph Pathfinding Algorithms

Implementation of Dijkstra's algorithm and A* search in Python, applied to weighted graphs and grid-based pathfinding. Built as part of CS2516 - Algorithms and Data Structures II.

Finds shortest paths in weighted graphs and grid environments, with support for vertex costs. A* uses a Manhattan distance heuristic to reduce the search space by up to 67% compared to standard Dijkstra. Includes two priority queue
implementations (binary min-heap and unsorted list) with benchmarking.

How to run

Dijkstra on simple graphs:

 python3 test_dijkstra.py

Grid pathfinding, A*, vertex costs, benchmarking:

 python3 processgrid.py

Requirements

 pip install matplotlib numpy
