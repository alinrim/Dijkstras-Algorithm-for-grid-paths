from pathlib import Path
from graphADT import Graph
from visualize import Animation
from heap import AdaptablePriorityQueue, UnsortedListAPQ
import time


def import_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    data = f.readline().split(',')
    rows = int(data[0])
    columns = int(data[1])
    print("rows: ", rows, "; columns: ", columns)
    grid = []
    start = None
    finish = None
    for r in range(rows):
        line = f.readline().split(',')
        grid.append([])
        for c in range(columns):
            val = line[c].strip()
            if val == 'X':
                grid[-1].append('X')
            else:
                grid[-1].append(val)
                if val == 'F':
                    finish = (r, c)
                elif val == 'S':
                    start = (r, c)
    f.close()
    if start is None or finish is None:
        print("ERROR: start =", start, "; finish =", finish)
        exit(1)
    return grid, start, finish


def runsearch(file, show_animation=True, apq_class=AdaptablePriorityQueue):
    grid, start, finish = import_instance(file)

    print("\n" + "="*60)
    print(f"File: {file}  |  APQ: {apq_class.__name__}")
    print("="*60)

    t0 = time.time()
    graph = Graph()
    graph.create_from_grid(grid)
    graph_time = time.time() - t0
    print(f"Graph created in {graph_time:.6f}s  "
          f"({graph.num_vertices()} vertices, {graph.num_edges()} edges)")

    sv = graph.get_vertex_by_label(start)
    fv = graph.get_vertex_by_label(finish)

    t0 = time.time()
    pd, rem_d, add_d = graph.dijkstra_dest_apq(sv, fv, apq_class=apq_class)
    dijkstra_time = time.time() - t0

    path_d, cost_d = graph.extract_path(pd, finish)
    print(f"\nDijkstra  {dijkstra_time:.6f}s | "
          f"APQ adds: {add_d} | removals: {rem_d} | "
          f"path cost: {cost_d} | path len: {len(path_d) if path_d else 'N/A'}")

    t0 = time.time()
    pa, rem_a, add_a = graph.a_star_apq(sv, fv, apq_class=apq_class)
    astar_time = time.time() - t0

    path_a, cost_a = graph.extract_path(pa, finish)
    print(f"A*        {astar_time:.6f}s | "
          f"APQ adds: {add_a} | removals: {rem_a} | "
          f"path cost: {cost_a} | path len: {len(path_a) if path_a else 'N/A'}")

    if cost_d != cost_a:
        print(f"  WARNING: cost mismatch -- Dijkstra={cost_d}, A*={cost_a}")
    else:
        print(f"  Both algorithms agree on cost: {cost_d}")

    if show_animation and path_a:
        animation = Animation(grid, start, finish, path_a)
        animation.show()

    return {
        'graph_time': graph_time,
        'dijkstra_time': dijkstra_time, 'dijkstra_removals': rem_d, 'dijkstra_additions': add_d,
        'astar_time':    astar_time,    'astar_removals':    rem_a, 'astar_additions':    add_a,
        'cost': cost_d,
    }


def challenge_comparison(files):
    print("\n" + "#"*60)
    print("Q5 CHALLENGE: Heap APQ vs Unsorted List APQ")
    print("#"*60)

    for f in files:
        print(f"\n{'-'*60}")
        print(f"Grid: {f}")
        grid, start, finish = import_instance(f)

        graph_heap = Graph()
        graph_heap.create_from_grid(grid)
        sv = graph_heap.get_vertex_by_label(start)
        fv = graph_heap.get_vertex_by_label(finish)

        for label, apq_cls in [('HeapAPQ ', AdaptablePriorityQueue),
                                ('ListAPQ ', UnsortedListAPQ)]:
            t0 = time.time()
            pd, rem_d, add_d = graph_heap.dijkstra_dest_apq(sv, fv, apq_class=apq_cls)
            dt = time.time() - t0
            _, cost = graph_heap.extract_path(pd, finish)

            t0 = time.time()
            pa, rem_a, add_a = graph_heap.a_star_apq(sv, fv, apq_class=apq_cls)
            at = time.time() - t0

            print(f"  {label} | Dijkstra {dt:.6f}s adds={add_d} rems={rem_d} | "
                  f"A* {at:.6f}s adds={add_a} rems={rem_a} | cost={cost}")


if __name__ == '__main__':
    BASIC_GRIDS = ['grid1basic.csv', 'grid2basic.csv', 'grid3basic.csv']
    COST_GRIDS  = ['grid1costs.csv', 'grid2costs.csv', 'grid3costs.csv']
    ALL_GRIDS   = BASIC_GRIDS + COST_GRIDS

    print("\n" + "="*60)
    print("Q2/Q3 — Basic grids (all edge costs = 1, no vertex costs)")
    print("="*60)
    for f in BASIC_GRIDS:
        runsearch(f, show_animation=True)

    print("\n" + "="*60)
    print("Q4 — Cost grids (edge costs = 1, vertex costs vary)")
    print("="*60)
    for f in COST_GRIDS:
        runsearch(f, show_animation=True)

    # Q5 challenge
    challenge_comparison(ALL_GRIDS)