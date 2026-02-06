import networkx as nx
from collections import deque

#--Parte per il calcolo del decremento minimo

#funnzione che dato un grafo e due nodi mi restituisce il percorso ottimo e tutti gli archi con i relativi pesi di quel percorso
def find_shortest_path(T, v, u):
    path = nx.shortest_path(T, v, u)
    if path is None:
        return None, None
    
    path_edges = []
    for i in range(len(path) - 1):
        a, b = path[i], path[i+1]
        weight = T[a][b].get('weight', 1)
        path_edges.append(((a, b), weight))
    return path, path_edges

#restisce l'arco con il costo massimo nel percorso ottimale
def find_max_path_edge(T, u, v):
    path, path_edges = find_shortest_path(T, v, u)

    if path is None or path_edges is None:
        return None, float('-inf')
    
    result = max(path_edges, key=lambda x: x[1])
    return result[0], result[1]
                             
#dato un arco restiusce il minimo decremento per entrare nel MST
def min_decrement(G, T, edge):
    u, v = edge

    if T.has_edge(u, v):
        return None
    
    edge_weight = G[u][v].get('weight', 1)
    max_edge, max_weight = find_max_path_edge(T, u, v)
    #trovando l'arco piu costoso nel percorso ottimo la quantità che dovrò diminuire dovrà essere almeno pari al valore di quel arco in modo da poter sostiuirlo
    if edge_weight <= max_weight:
        #nel caso gli arci siano uguali mi basta che il mio valore sia inferiore di 1 per assicurarmi di essere nella soluzione ottima
        min_decrement = 1
    else:
        min_decrement = edge_weight - max_weight + 1

    return min_decrement
#esegue il controllo del minimo decremento su tutti gli archi (se presenti nel MST il loro decremento minimo sarà 0 essendo gia in soluzione)
def find_graf_min_dec(G, T):
    results = []

    for u, v in G.edges():
        if T.has_edge(u, v):
            results.append(((u, v), 0))
        else:
            results.append(((u, v), min_decrement(G, T, (u, v))))
    return results


#---Parte per il calcolo del massimo aumento

#funzione che restituisce il massimo incremento consentito ad un arco
def max_increase(G, T, edge):
    u, v = edge

    # controllo che l'arco appartenga al MST
    if not T.has_edge(u, v):
        return None

    weight = T[u][v].get('weight', 1)

    #creo un nuovo grafo senza quel arco
    T_temp = T.copy()
    T_temp.remove_edge(u, v)

    # avendo separato MST mi trovo con due grafi scollegati
    graphs = list(nx.connected_components(T_temp))
    #caso di errore non vengano creati due grafi allora MST era sbagliato
    if len(graphs) != 2:
        return None
    #per maggiore comodita faccio in modo che u sia sempre dentro C1
    C1, C2 = graphs
    if u not in C1:
        C1, C2 = C2, C1

    min_cross_weight = float('inf')

    #scorro tutti gli archi nel grafo
    for x, y, data in G.edges(data=True):
        #se i due nodi del arco si trovano nei due grafi separati
        if (x in C1 and y in C2) or (x in C2 and y in C1):
            #e non sono il grafo che stavo considerando
            if not (x == u and y == v):
                #aggiorno il peso nel caso sia l'arco trovato abbia un peso minore rispetto a quelli prima
                w = data.get('weight', 1)
                min_cross_weight = min(min_cross_weight, w)

    # se non esiste un acro che possa sostiurire allora potrò aumentare il peso al infinito
    if min_cross_weight == float('inf'):
        return float('inf')

    # incremento massimo consentito in modo rimanga dentro l'MST
    return min_cross_weight - weight

#applica il calcolo del massimo incremento a tutti gli archi in soluzione
def find_graf_max_inc(G, T):
    results = []
    for u, v in T.edges():
        results.append(((u, v), max_increase(G, T, (u, v))))
    return results
