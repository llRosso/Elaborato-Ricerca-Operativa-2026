import matplotlib.pyplot as plt
import networkx as nx

DEFAULT_FIGSIZE = (12, 8)
DEFAULT_NODE_SIZE = 500
DEFAULT_FONT_SIZE = 10

#stili degli archi in base al loro ruolo
EDGE_STYLE_DEFAULT = {"color": "gray", "style": "dashed", "width": 1}
EDGE_STYLE_MST = {"color": "red", "style": "solid", "width": 3}
EDGE_STYLE_CURRENT = {"color": "green", "style": "dashed", "width": 4}
EDGE_STYLE_ADJACENT = {"color": "purple", "style": "dotted", "width": 2}

#restituisce le posizioni dei nodi secondo il layout richiesto
def compute_layout(G, layout_type: str = "spring", seed: int = 42) -> dict:
    layout_map = {
        "spring": lambda g: nx.spring_layout(g, seed=seed),
        "circular": nx.circular_layout,
        "kamada_kawai": nx.kamada_kawai_layout,
        "random": lambda g: nx.random_layout(g, seed=seed),
        "shell": nx.shell_layout,
    }
    # se il layout richiesto non esiste, usa spring di default
    layout_func = layout_map.get(layout_type, layout_map["spring"])
    return layout_func(G)

#crea figura matplotlib e l'asse di disegno, restituisce la coppia (fig, ax)
def create_figure(figsize: tuple = DEFAULT_FIGSIZE):
    return plt.subplots(figsize=figsize)

# aggiunge titolo, info-box e nasconde gli assi
def finalize_figure(ax, title: str, info_lines: list[str],
                    font_size: int = DEFAULT_FONT_SIZE):
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)

    #se presenti, mostra le informazioni laterali
    if info_lines:
        info_text = "\n".join(info_lines)
        ax.text(
            1.02, 0.98, info_text,
            transform=ax.transAxes, fontsize=font_size - 1,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    ax.axis("off")
    plt.tight_layout()

#assegna uno stile a ciascun arco in base al suo stato
def classify_edges(G, mst=None, current_edge=None,
                   current_node=None) -> list[dict]:
    styles = []
    for u, v in G.edges():
        #l'arco è attualmente analizzato
        if current_edge and {u, v} == set(current_edge):
            styles.append(EDGE_STYLE_CURRENT)
        #l'arco è in soluzione
        elif mst and mst.has_edge(u, v):
            styles.append(EDGE_STYLE_MST)
        # arco adiacente al nodo corrente (usato in Prim)
        elif current_node and (u == current_node or v == current_node):
            styles.append(EDGE_STYLE_ADJACENT)
        # stile di default
        else:
            styles.append(EDGE_STYLE_DEFAULT)
    return styles

# disegna tutti gli archi del grafo usando gli stili assegnati
def draw_edges(G, pos, edge_styles: list[dict], ax):
    for (u, v), style in zip(G.edges(), edge_styles):
        nx.draw_networkx_edges(
            G, pos, edgelist=[(u, v)],
            edge_color=style["color"],
            style=style["style"],
            width=style["width"],
            alpha=0.8, ax=ax,
        )

# disegna i nodi del grafo
def draw_nodes(G, pos, ax, node_colors="lightblue",
               edge_colors="black", node_size=DEFAULT_NODE_SIZE,
               linewidths=2):
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        edgecolors=edge_colors,
        node_size=node_size,
        linewidths=linewidths,
        alpha=0.9, ax=ax,
    )

#aggiunge le etichette sui nodi
def draw_labels(G, pos, ax, font_size=DEFAULT_FONT_SIZE, font_color="black"):
    nx.draw_networkx_labels(
        G, pos,
        font_size=font_size,
        font_weight="bold",
        font_color=font_color,
        ax=ax,
    )

# disegna le etichette sugli archi
def draw_edge_weights(G, pos, ax, font_size=DEFAULT_FONT_SIZE):
    edge_labels = {
        (u, v): G[u][v]["weight"]
        for u, v in G.edges()
        if "weight" in G[u][v]
    }
    if edge_labels:
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels,
            font_color="darkblue",
            font_size=font_size - 2,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8),
            ax=ax,
        )

#disegna un grafo base
def draw_graph(G, title="Grafo" ,node_size=DEFAULT_NODE_SIZE, 
               font_size=DEFAULT_FONT_SIZE,
               figsize=DEFAULT_FIGSIZE):
    
    pos = compute_layout(G, "circular")

    fig, ax = create_figure(figsize)

    edge_styles = classify_edges(G)
    draw_edges(G, pos, edge_styles, ax)
    draw_nodes(G, pos, ax, node_size=node_size, edge_colors="black", linewidths=1)
    draw_labels(G, pos, ax, font_size=font_size)
    draw_edge_weights(G, pos, ax, font_size=font_size)
    # info di base nella lablel laterale del grafo
    info_lines = [
        f"Nodi: {G.number_of_nodes()}",
        f"Archi: {G.number_of_edges()}",
    ]
    finalize_figure(ax, title, info_lines, font_size)
    plt.show()
    return pos, fig, ax

#disegna il grafo per rappresentare i vari passaggi del algoritmo di kruskal
def draw_graph_kruskal(G, mst=None, components=None,
                       current_edge=None, title="Grafo – Kruskal"):
    pos = compute_layout(G, "circular")
    fig, ax = create_figure((12, 8))

    edge_styles = classify_edges(G, mst=mst, current_edge=current_edge)
    draw_edges(G, pos, edge_styles, ax)
    draw_nodes(G, pos, ax, node_size=800)
    draw_labels(G, pos, ax, font_size=14)
    draw_edge_weights(G, pos, ax, font_size=11)

    # etichette delle componenti connesse per ogni nodo
    if components:
        for node, (x, y) in pos.items():
            ax.text(
                x, y + 0.08, f"Comp: {components[node] + 1}",
                fontsize=10, fontweight="bold", color="darkred",
                ha="center", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black",
                          alpha=0.8, linewidth=1),
            )

    # info nella lablel laterale del grafo
    info_lines = [
        f"Nodi: {G.number_of_nodes()}",
        f"Archi: {G.number_of_edges()}",
    ]
    if current_edge:
        u, v = current_edge
        weight = G[u][v].get("weight", "N/A")
        info_lines += ["", f"Arco corrente:", f"{u}-{v} (peso: {weight})"]

    finalize_figure(ax, title, info_lines)
    plt.show()
    return pos, fig, ax

#disegna il grafo per rappresentare i vari passaggi del algoritmo di prim
def draw_graph_prim(G, mst=None, distances=None,
                    predecessors=None, current_node=None,
                    current_edge=None, title="Prim Algorithm"):
    
    pos = compute_layout(G, "circular")

    fig, ax = create_figure((14, 10))

    edge_styles = classify_edges(G, mst=mst, current_edge=current_edge, current_node=current_node)
    draw_edges(G, pos, edge_styles, ax)
    draw_nodes(G, pos, ax, node_size=800)
    draw_labels(G, pos, ax, font_size=16)
    draw_edge_weights(G, pos, ax, font_size=11)

    # lableling per ogni nodo
    for node, (x, y) in pos.items():
        dist = distances.get(node, float("inf")) if distances else float("inf")

        # mostra il valore della distnza se definito
        if dist != float("inf"):
            ax.text(
                x - 0.008, y - 0.08, f"Dist: {dist}",
                fontsize=10, fontweight="bold", color="darkred",
                ha="right", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow",
                          edgecolor="darkred", alpha=0.8, linewidth=1),
            )

        #aggiunge etichetta predecessore se presente
        if predecessors and predecessors.get(node) is not None:
            ax.text(
                x + 0.008, y - 0.08, f"Pred: {predecessors[node]}",
                fontsize=10, fontweight="bold", color="darkblue",
                ha="left", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue",
                          edgecolor="darkblue", alpha=0.8, linewidth=1),
            )

    # info nella lablel laterale del grafo
    info_lines = [
        f"Nodi: {G.number_of_nodes()}",
        f"Archi: {G.number_of_edges()}",
    ]

    # informazioni sull'MST parziale
    if mst:
        mst_weight = sum(mst[u][v].get("weight", 1) for u, v in mst.edges())
        info_lines += ["", f"MST parziale:", f"Archi: {mst.number_of_edges()}",
                       f"Peso: {mst_weight:.0f}"]

    # informazioni sul nodo corrente
    if current_node:
        info_lines += ["", f"Nodo corrente: {current_node}"]
        if distances and distances.get(current_node, float("inf")) != float("inf"):
            info_lines.append(f"L[{current_node}] = {distances[current_node]}")
        if predecessors and predecessors.get(current_node):
            info_lines.append(f"pred[{current_node}] = {predecessors[current_node]}")

    finalize_figure(ax, title, info_lines)
    plt.show()
    return pos, fig, ax