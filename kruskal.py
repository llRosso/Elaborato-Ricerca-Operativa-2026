import networkx as nx
import matplotlib.pyplot as plt
from draw import draw_graph_kruskal

def kruskal_mst(G):
    #funzione per disegnare il grafo
    def draw(title, current_edge):
        draw_graph_kruskal(
            G, mst=T, components=comp_dict,
            current_edge=current_edge, title=title
        )
    
    #verifica se il grafo è conneso
    if not nx.is_connected(G):
        print("grafo non conneso")
        return None
    
    #creo grafo MST
    T = nx.Graph()
    T.add_nodes_from(G.nodes())
    
    #ordino i lati per peso
    edges = sorted(G.edges(data=True), key=lambda x: x[2].get('weight', 1))
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    node_to_id = {node: i for i, node in enumerate(nodes)}
    comp_list = list(range(n))
    #ad ogni nodo associo una label che al inizio rappresenta se stesso
    comp_dict = {node: comp_list[node_to_id[node]] for node in nodes}
    
    k = 0
    h = 0
    m = len(edges)
    step = 1
    #ciclo per il numero di nodi meno uno e il numero di archi
    while k < n - 1 and h < m:
        #seleziono un lato
        i, j, data = edges[h]
        weight = data.get('weight', 1)
        current_edge = (i, j)
        
        id_i, id_j = node_to_id[i], node_to_id[j]
        #prendo le componeti dei due nodi associari al arco
        C1, C2 = comp_list[id_i], comp_list[id_j]
        #controllo che siano diversi le componeti
        added = C1 != C2

        #disegno questa scelta
        title = f"Kruskal - Passo {step}\nArco: {i}-{j} (peso: {weight}) - "
        title += "AGGREGATO" if added else "SCARTATO"
        draw(title, current_edge)
        
        if added:
            #se sono diversi aggiungo al albero MST l'arco
            T.add_edge(i, j, weight=weight)
            k += 1
            #uniico le due componenti c1 e c2 e modificando anche tutti i nodi con le stesse componenti in modo in modo che rimanga solo uno dei due eventuali gruppi
            for q in range(n):
                if comp_list[q] == C2:
                    comp_list[q] = C1
            #aggiorno anche il dizionario per corrispondere alla lista dei componeti
            comp_dict = {node: comp_list[node_to_id[node]] for node in nodes}
        
        h += 1
        step += 1
    
    # disegno grafo finale
    total_weight = sum(T[u][v].get('weight', 1) for u, v in T.edges())
    title=f"MST FINALE - Peso totale: {total_weight}"
    draw(title, None)
    
    return T