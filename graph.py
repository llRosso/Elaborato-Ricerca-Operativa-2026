import networkx as nx

graphs = [((
        (1, 2, 3),  # peso 3
        (1, 3, 5),  # peso 5
        (2, 3, 1),  # peso 1
        (2, 4, 6),  # peso 6
        (3, 4, 4),  # peso 4
        (3, 5, 2),  # peso 2
        (4, 5, 7)   # peso 7
        ), 5),
        ((
        (1, 2, 2),
        (1, 7, 5),
        (1, 8, 1),
        (2, 3, 0),
        (2, 7, 4),
        (3, 7, 5),
        (3, 4, 1),
        (4, 5, 3),
        (4, 6, 2),
        (4, 7, 10),
        (5, 6, 6),
        (5, 8, 2),
        (6, 8, 1),
        (7, 8, 0),
        ), 8)]

def create_graph(num):
    if(num > number_of_graphs()):
        return None

    G = nx.Graph()
    edges = graphs[num-1][0]
    
    G.add_nodes_from(range(1, graphs[num-1][1]+1))
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    return G

def number_of_graphs():
    return len(graphs)