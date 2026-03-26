from graphADT import Graph

def parse_simplegraph(filename):
    g = Graph()
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                i += 1
                if not line:
                    continue
                if line.startswith('Node'):
                    id_line = lines[i].strip()
                    i += 1
                    parts = id_line.split(':')
                    if len(parts) == 2:
                        node_id = int(parts[1].strip())
                        g.add_vertex_if_new(node_id)
                elif line.startswith('Edge'):
                    from_id = None
                    to_id = None
                    length = None
                    for _ in range(4):
                        if i < len(lines):
                            prop_line = lines[i].strip()
                            i += 1
                            if prop_line.startswith('from:'):
                                from_id = int(prop_line.split(':')[1].strip())
                            elif prop_line.startswith('to:'):
                                to_id = int(prop_line.split(':')[1].strip())
                            elif prop_line.startswith('length:'):
                                length = int(prop_line.split(':')[1].strip())
                    if from_id is not None and to_id is not None and length is not None:
                        v_from = g.get_vertex_by_label(from_id)
                        v_to = g.get_vertex_by_label(to_id)
                        if v_from and v_to:
                            g.add_edge(v_from, v_to, length)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None
    return g