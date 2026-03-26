from parse_simplegraph import parse_simplegraph
from graphADT import Graph
from dijkstra import dijkstra

def test_simplegraph1():
    print("\n" + "="*60)
    print("Testing on simplegraph1.txt")
    print("="*60)
    g = parse_simplegraph('simplegraph1.txt')
    if g is None:
        return
    print(f"Graph loaded: {g.num_vertices()} vertices, {g.num_edges()} edges")
    source = g.get_vertex_by_label(1)
    target = g.get_vertex_by_label(4)
    if source is None or target is None:
        print("ERROR: Could not find source or target vertex")
        return
    result = dijkstra(g, source)
    if target in result:
        predecessor, cost = result[target]
        print(f"\nShortest path from 1 to 4:")
        print(f"  Cost: {cost}")
        print(f"  Predecessor: {predecessor.element() if predecessor else None}")
        if cost == 8 and predecessor.element() == 3:
            print("  correct")
        else:
            print("  incorrect (expected cost=8, predecessor=3)")
    else:
        print("ERROR: Target vertex not reachable")
    print("\nAll shortest paths from vertex 1:")
    for v in sorted(result.keys(), key=lambda x: x.element()):
        pred, cost = result[v]
        pred_label = pred.element() if pred else "None"
        print(f"  To {v.element()}: cost={cost}, predecessor={pred_label}")


def test_simplegraph2():
    print("\n" + "="*60)
    print("Testing on simplegraph2.txt")
    print("="*60)
    g = parse_simplegraph('simplegraph2.txt')
    if g is None:
        return
    print(f"Graph loaded: {g.num_vertices()} vertices, {g.num_edges()} edges")
    source = g.get_vertex_by_label(14)
    target = g.get_vertex_by_label(5)
    if source is None or target is None:
        print("ERROR: Could not find source or target vertex")
        return
    result = dijkstra(g, source)
    if target in result:
        predecessor, cost = result[target]
        print(f"\nShortest path from 14 to 5:")
        print(f"  Cost: {cost}")
        print(f"  Predecessor: {predecessor.element() if predecessor else None}")
        if cost == 16 and predecessor.element() == 8:
            print("  correct")
        else:
            print("  incorrect (expected cost=16, predecessor=8)")
    else:
        print("ERROR: Target vertex not reachable")
    print(f"\nReachable vertices from 14: {len(result)} vertices")


if __name__ == '__main__':
    test_simplegraph1()
    test_simplegraph2()