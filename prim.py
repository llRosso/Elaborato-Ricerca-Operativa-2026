import networkx as nx
import matplotlib.pyplot as plt
from draw import draw_graph_prim

def prim_mst(G, start_node=1):
    #funzione per il disegno del grafo
    def draw(title, current_node = None, current_edge = None):
        draw_graph_prim(G, T, L, pred,
                       current_node=current_node,
                       current_edge=current_edge,
                       title=title)
    
    #verifico se il grafo è connesso
    if not nx.is_connected(G):
        print("grafo non conneso")
        return None
    
    #verifico se il nodo di partenza è presente nel grafo
    if start_node not in G.nodes():
        print(f"Il nodo {start_node} non esiste nel grafo")
        return None
    
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    
    # Inizializzazione
    #flag indica se il nodo è gia stato preso o no
    flag = {node: False for node in nodes}
    #pred inidica il predecessore del nodo nell’albero MST (nodo tramite cui si ottiene il costo minimo)
    pred = {node: None for node in nodes}
    #L indica la distnza di un nodo, inifinito se il nodo non è attualmente raggiungilile 
    L = {node: float('inf') for node in nodes}
    
    #inidico come gia preso il nodo di partenza, il nodo di arrivo è se stesso, la distanza è 0
    flag[start_node] = True
    pred[start_node] = start_node
    L[start_node] = 0
    
    for node in nodes:
        #per tutti i nodi al difuori di quello di partenza il nodo di arrivo è quello di partenza
        if node != start_node:
            pred[node] = start_node
            #se il nodo è conneso al nodo di partenza gli aggiorno gia il peso
            if G.has_edge(start_node, node):
                L[node] = G[start_node][node].get('weight', 1)
    
    #creo il nuovo grafo del mst e ci aggiungo gia il nodo di partenza
    T = nx.Graph()
    T.add_node(start_node)

    #disegno la prima volta il grafo
    step = 1
    title = f"Prim - Passo 0: Inizializzazione\nS = {{{start_node}}}"
    draw(title, start_node, None)
    
    for k in range(1, n):
        min_dist = float('inf')
        h = None
        #scorro tutti inodi non gia selezionati e prendo quello con la distnza minore
        for node in nodes:
            if not flag[node] and L[node] < min_dist:
                min_dist = L[node]
                h = node
        #nel caso non l'abbia trovato interompo
        if h is None:
            break
        
        # eventuale arco da aggiungere
        edge_to_add = (pred[h], h) if pred[h] != h else None

        #disegno la nuova selezione
        title = f"Prim - Passo {step}: Selezione nodo\n"
        title += f"Selezionato nodo {h} con L[{h}] = {min_dist}"
        draw(title, h, edge_to_add)

        step += 1
        
        # Aggiungi nodo all'MST
        flag[h] = True
        if pred[h] != h:
            T.add_edge(pred[h], h, weight=G[pred[h]][h].get('weight', 1))
        
        # Aggiorna distanze e i nodi di arrivo dei nodi adiacenti
        for node in nodes:
            #verifico che il nodo non sia gia stato preso ed esista un arco tra l'arco aggiornato e il nodo
            if not flag[node] and G.has_edge(h, node):
                weight = G[h][node].get('weight', 1)
                #se il suo peso è inferiore aggiorno
                if weight < L[node]:
                    L[node] = weight
                    pred[node] = h
            
    # Visualizzazione finale
    total_weight = sum(T[u][v].get('weight', 1) for u, v in T.edges())
    title = f"Prim - MST FINALE\nPeso totale: {total_weight}"
    draw(title, None, None)

    return T