from heap import AdaptablePriorityQueue

class vertex:
    def __init__(self, element, cost=0):
        self._element = element
        self._cost = cost
    def __str__(self):
        return str(self._element)
    def element(self):
        return self._element
    def cost(self):
        return self._cost
    def set_cost(self, cost):
        self._cost = cost

class edge:
    def __init__(self, u, v, element):
        self._u = u 
        self._v = v
        self._element = element
    def __str__(self):
        return "(" + str(self._u) + "--" + str(self._v) + ")"
    def vertices(self):
        return self._u, self._v
    def opposite(self, x):
        if x is self._u: return self._v
        if x is self._v: return self._u
        return None
    def element(self):
        return self._element

class Graph:
    def __init__(self):
        self._structure = {}
        self._vertex_map = {}
        self._edge_list = []
        
    def num_vertices(self): return len(self._structure)
    def num_edges(self): return len(self._edge_list)
    def vertices(self): return list(self._structure.keys())
    def edges(self): return self._edge_list

    def get_vertex_by_label(self, label):
        return self._vertex_map.get(label)

    def get_edge(self, x, y):
        return self._structure.get(x, {}).get(y)

    def degree(self, x):
        return len(self._structure[x])

    def get_edges(self, x):
        if x not in self._structure: return None
        return list(self._structure[x].values())
        
    def add_vertex(self, element, cost=0):
        v = vertex(element, cost)
        self._structure[v] = {}
        self._vertex_map[element] = v
        return v
    
    def add_vertex_if_new(self, element, cost=0):
        v = self.get_vertex_by_label(element)
        if v is None:
            v = self.add_vertex(element, cost)
        return v
    
    def add_edge(self, v, w, element):
        if v not in self._structure or w not in self._structure:
            return None
        if w in self._structure[v]:
            return None
        new_edge = edge(v, w, element)
        self._structure[v][w] = new_edge
        self._structure[w][v] = new_edge
        self._edge_list.append(new_edge)
        return new_edge

    def create_from_grid(self, grid):
        rows = len(grid)
        columns = len(grid[0])
        for r in range(rows):
            for c in range(columns):
                if grid[r][c] != 'X':
                    if grid[r][c] == 'S' or grid[r][c] == 'F':
                        cost = 0
                    else:
                        try:
                            cost = int(grid[r][c])
                        except ValueError:
                            cost = 0
                    self.add_vertex((r, c), cost)
        for r in range(rows):
            for c in range(columns):
                if grid[r][c] != 'X':
                    vertex_obj = self.get_vertex_by_label((r, c))
                    if r+1 < rows and grid[r+1][c] != 'X':
                        other = self.get_vertex_by_label((r+1, c))
                        if other and self.get_edge(vertex_obj, other) is None:
                            self.add_edge(vertex_obj, other, 1)
                    if c+1 < columns and grid[r][c+1] != 'X':
                        other = self.get_vertex_by_label((r, c+1))
                        if other and self.get_edge(vertex_obj, other) is None:
                            self.add_edge(vertex_obj, other, 1)
                    if r-1 >= 0 and grid[r-1][c] != 'X':
                        other = self.get_vertex_by_label((r-1, c))
                        if other and self.get_edge(vertex_obj, other) is None:
                            self.add_edge(vertex_obj, other, 1)
                    if c-1 >= 0 and grid[r][c-1] != 'X':
                        other = self.get_vertex_by_label((r, c-1))
                        if other and self.get_edge(vertex_obj, other) is None:
                            self.add_edge(vertex_obj, other, 1)

    def dijkstra_dest_apq(self, source, destination=None, apq_class=None):
        if apq_class is None:
            apq_class = AdaptablePriorityQueue

        distances   = {source: source.cost()}
        predecessors = {source: None}
        apq = apq_class()
        apq.add(source.cost(), source)
        additions = 1

        processed = set()
        removals  = 0

        while not apq.is_empty():
            result = apq.remove_min()
            if result is None:
                break
            cost, u = result

            if u in processed:
                continue
            processed.add(u)
            removals += 1

            for edge_obj in (self.get_edges(u) or []):
                v = edge_obj.opposite(u)
                if v in processed:
                    continue
                new_dist = distances[u] + edge_obj.element() + v.cost()
                if v not in distances:
                    distances[v]    = new_dist
                    predecessors[v] = u
                    apq.add(new_dist, v)
                    additions += 1
                elif new_dist < distances[v]:
                    distances[v]    = new_dist
                    predecessors[v] = u
                    apq.update(v, new_dist)

        result = {v: (predecessors[v], distances[v]) for v in distances}
        return result, removals, additions

    def a_star_apq(self, source, destination, apq_class=None):
        if apq_class is None:
            apq_class = AdaptablePriorityQueue

        distances    = {source: source.cost()}
        predecessors = {source: None}
        dest_label   = destination.element()
        apq = apq_class()
        additions = 1

        def heuristic(v):
            vl = v.element()
            return abs(vl[0] - dest_label[0]) + abs(vl[1] - dest_label[1])

        h = heuristic(source)
        apq.add((h + source.cost(), source.cost()), source)

        processed = set()
        removals  = 0

        while not apq.is_empty():
            result = apq.remove_min()
            if result is None:
                break
            priority, u = result

            if u in processed:
                continue
            processed.add(u)
            removals += 1

            if u is destination:
                break

            for edge_obj in (self.get_edges(u) or []):
                v = edge_obj.opposite(u)
                if v in processed:
                    continue
                new_dist = distances[u] + edge_obj.element() + v.cost()
                if v not in distances:
                    distances[v]    = new_dist
                    predecessors[v] = u
                    h = heuristic(v)
                    apq.add((new_dist + h, new_dist), v)
                    additions += 1
                elif new_dist < distances[v]:
                    distances[v]    = new_dist
                    predecessors[v] = u
                    h = heuristic(v)
                    apq.update(v, (new_dist + h, new_dist))

        result_dict = {v: (predecessors[v], distances[v]) for v in distances}
        return result_dict, removals, additions

    def extract_path(self, search_result, finish_coordinate):
        fv = self.get_vertex_by_label(finish_coordinate)
        if fv is None or fv not in search_result:
            return None, float('inf')

        path = []
        cost = search_result[fv][1]
        current = fv
        while current is not None:
            path.append(current.element())
            predecessor, _ = search_result[current]
            current = predecessor

        path.reverse()
        return path, cost

    def __str__(self):
        return f"Graph: {self.num_vertices()} vertices, {self.num_edges()} edges"

        
def test_graph():
    print()  
    print("-------------------------------------------")
    print("Testing on the simple 3-vertex 2-edge graph")
    print("-------------------------------------------")
    graph = Graph()
    a = graph.add_vertex('a', 0)
    b = graph.add_vertex('b', 5)
    c = graph.add_vertex('c', 3)
    d = graph.add_vertex_if_new('b', 0)   #should not create a vertex
    eab = graph.add_edge(a, b, 2)
    ebc = graph.add_edge(b, c, 9)

    vnone = vertex('dummy')
    evnone = graph.add_edge(vnone, c, 0)   #should not create an edge
    if evnone is not None:
        print('ERROR: attempted edges  should have been none')

    edges = graph.get_edges(vnone)     #should be None: vnone not in graph
    if edges != None:
        print('ERROR: returned edges for non-existent vertex.')
        
    print('number of vertices:', graph.num_vertices())
    print('number of edges:', graph.num_edges())

    print('Vertex list should be a,b,c in any order :')
    vertices = graph.vertices()
    for key in vertices:
        print(f'{key.element()} (cost: {key.cost()})')
    print('Edge list should be (a,b,2),(b,c,9) in any order :')
    edges = graph.edges()
    for edge_obj in edges:
        print(edge_obj)

    print('Graph display should repeat the above:')
    print(graph)

    v = graph.add_vertex('d', 7)
    edges = graph.get_edges(v)
    if edges != []:
        print('ERROR: should have returned an empty list, but got', edges)
    print('Graph should now have a new vertex d with no edges and cost 7')
    print(graph)

if __name__ == '__main__':
    test_graph()