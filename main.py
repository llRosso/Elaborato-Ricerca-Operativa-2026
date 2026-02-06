import networkx as nx
import matplotlib.pyplot as plt
from graph import create_graph, number_of_graphs
from kruskal import kruskal_mst
from prim import prim_mst
from draw import draw_graph
from cost_variable import find_graf_min_dec, find_graf_max_inc

def main():
    num = input(f"Sceliere un numero tra 1 e {number_of_graphs()} per selezionare tra i grafi presenti: ")
    # Crea grafo di esempio
    G = create_graph(int(num))
    if G is None:
        return
    
    print("Grafo iniziale:")
    print(f"Nodi: {G.number_of_nodes()} Archi: {G.number_of_edges()}")
    print(f"Archi con pesi: {[(u, v, G[u][v]['weight']) for u, v in G.edges()]}")
    # Visualizza grafo iniziale
    draw_graph(G, title="Grafo Iniziale")
    

    mst_k = kruskal_mst(G)
    print("\nMST trovato con Kruskal:")
    print(f"Archi: {[(u, v) for u, v in mst_k.edges()]}")
    print(f"Costo totale: {sum(mst_k[u][v]['weight'] for u, v in mst_k.edges())}")
    
    mst_p = prim_mst(G, start_node=1)
    print("\nMST trovato con Prim:")
    print(f"Archi: {[(u, v) for u, v in mst_p.edges()]}")
    print(f"Costo totale: {sum(mst_p[u][v]['weight'] for u, v in mst_p.edges())}")
    
    # Algortimo gia presente nella libreria networkx il gli MST, si basa su kruskal
    mst_nx = nx.minimum_spanning_tree(G)
    print("\nMST trovato con funzione libreria:")
    print(f"Archi: {[(u, v) for u, v in mst_nx.edges()]}")
    print(f"Costo totale: {sum(mst_nx[u][v]['weight'] for u, v in mst_nx.edges())}")
    
    print("\n--- Massimo Incremento ---")
    result = find_graf_max_inc(G, mst_nx)
    print(f"Archi: {[edge for edge in result]}")

    print("\n--- Minimo Decremento ---")
    result = find_graf_min_dec(G, mst_nx)
    print(f"Archi: {[edge for edge in result]}")

if __name__ == "__main__":
    main()