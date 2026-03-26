from heap import AdaptablePriorityQueue

def dijkstra(graph, source):
    distances = {source: 0}
    predecessors = {source: None}
    apq = AdaptablePriorityQueue()
    apq.add(0, source)
    processed = set()
    
    while not apq.is_empty():
        result = apq.remove_min()
        if result is None:
            break
        cost, u = result
        if u in processed:
            continue
        processed.add(u)
        edges = graph.get_edges(u)
        if edges:
            for edge_obj in edges:
                v = edge_obj.opposite(u)
                if v in processed:
                    continue
                new_distance = distances[u] + edge_obj.element() + v.cost()
                if v not in distances:
                    distances[v] = new_distance
                    predecessors[v] = u
                    apq.add(new_distance, v)
                elif new_distance < distances[v]:
                    distances[v] = new_distance
                    predecessors[v] = u
                    apq.update(v, new_distance)
    
    result = {}
    for vertex in distances:
        result[vertex] = (predecessors[vertex], distances[vertex])
    return result