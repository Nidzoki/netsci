import marimo

__generated_with = "0.19.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exercise 02: Facebook Ego Network

    This notebook uses one ego network from the SNAP Facebook social-circles collection.
    I use ego **698** because it is small enough to visualize clearly while still showing visible clustering in the local neighborhood.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import pandas as pd
    return Path, np, nx, pd, plt


@app.cell
def _(Path):
    EGO_ID = 698
    NOTEBOOK_DIR = (
        Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    )
    DATA_DIR = NOTEBOOK_DIR / "facebook"
    EDGE_PATH = DATA_DIR / f"{EGO_ID}.edges"
    CIRCLE_PATH = DATA_DIR / f"{EGO_ID}.circles"
    return CIRCLE_PATH, EDGE_PATH, EGO_ID


@app.cell
def _(nx):
    def load_ego_network(edge_path, ego_id):
        graph = nx.read_edgelist(edge_path, nodetype=int, create_using=nx.Graph())
        alters = list(graph.nodes())
        graph.add_node(ego_id)
        graph.add_edges_from((ego_id, alter) for alter in alters)
        return graph
    return (load_ego_network,)


@app.cell
def _(CIRCLE_PATH):
    annotated_circles = {}

    if CIRCLE_PATH.exists():
        with CIRCLE_PATH.open() as file:
            for line in file:
                parts = line.split()
                if parts:
                    annotated_circles[parts[0]] = [int(node) for node in parts[1:]]

    circle_sizes = sorted(
        (len(nodes) for nodes in annotated_circles.values()),
        reverse=True,
    )
    return (annotated_circles,)


@app.cell
def _(EDGE_PATH, EGO_ID, load_ego_network, nx):
    G = load_ego_network(EDGE_PATH, EGO_ID)
    alters = sorted(node for node in G.nodes() if node != EGO_ID)
    alter_graph = nx.subgraph(G, alters).copy()
    alter_components = sorted(
        nx.connected_components(alter_graph),
        key=len,
        reverse=True,
    )
    component_sizes = [len(component) for component in alter_components]
    return G, alter_components, alter_graph, component_sizes


@app.cell
def _(EGO_ID, G, alter_components, annotated_circles, nx, pd):
    density = nx.density(G)
    degree_series = pd.Series(dict(G.degree()), name="degree").sort_values(
        ascending=False
    )

    metrics_df = pd.DataFrame(
        [
            {"metric": "ego id", "value": EGO_ID},
            {"metric": "nodes", "value": G.number_of_nodes()},
            {"metric": "edges", "value": G.number_of_edges()},
            {"metric": "density", "value": round(density, 4)},
            {"metric": "connected", "value": nx.is_connected(G)},
            {"metric": "connected components", "value": nx.number_connected_components(G)},
            {"metric": "components without ego", "value": len(alter_components)},
            {"metric": "annotated circles in SNAP file", "value": len(annotated_circles)},
        ]
    )

    degree_stats_df = pd.DataFrame(
        [
            {"stat": "minimum degree", "value": int(degree_series.min())},
            {"stat": "25th percentile", "value": round(float(degree_series.quantile(0.25)), 2)},
            {"stat": "median degree", "value": round(float(degree_series.median()), 2)},
            {"stat": "mean degree", "value": round(float(degree_series.mean()), 2)},
            {"stat": "75th percentile", "value": round(float(degree_series.quantile(0.75)), 2)},
            {"stat": "maximum degree", "value": int(degree_series.max())},
        ]
    )

    top_degree_df = degree_series.head(10).rename_axis("node").reset_index()
    top_degree_df["is_ego"] = top_degree_df["node"].eq(EGO_ID)
    return degree_series, degree_stats_df, density, metrics_df, top_degree_df


@app.cell
def _(component_sizes, pd):
    component_df = pd.DataFrame(
        {
            "alter component": [
                f"component {index}" for index in range(1, len(component_sizes) + 1)
            ],
            "size": component_sizes,
        }
    )
    return (component_df,)


@app.cell(hide_code=True)
def _(G, component_sizes, density, mo):
    def _():
        sizes_text = ", ".join(str(size) for size in component_sizes)
        return mo.md(
            f"""
            The graph contains **{G.number_of_nodes()} nodes** and **{G.number_of_edges()} edges**.
            Its density is **{density:.4f}** and the full ego network is **connected**.
            If the ego node is removed, the alters split into connected pieces of sizes **{sizes_text}**.
            """
        )


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Graph Summary
    """)
    return


@app.cell
def _(metrics_df):
    metrics_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Degree Distribution Basics
    """)
    return


@app.cell
def _(degree_stats_df):
    degree_stats_df
    return


@app.cell
def _(top_degree_df):
    top_degree_df
    return


@app.cell
def _(EGO_ID, G, degree_series, plt):
    def _():
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(degree_series.values, bins=12, color="#4C78A8", edgecolor="white")
        ax.axvline(
            G.degree(EGO_ID),
            color="#D1495B",
            linestyle="--",
            linewidth=2,
            label=f"ego degree = {G.degree(EGO_ID)}",
        )
        ax.set_title("Degree distribution")
        ax.set_xlabel("Degree")
        ax.set_ylabel("Number of nodes")
        ax.legend(frameon=False)
        fig.tight_layout()
        return fig


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Alter Components After Removing the Ego
    """)
    return


@app.cell
def _(component_df):
    component_df
    return


@app.cell
def _(EGO_ID, G, alter_components, alter_graph, np, nx, plt):
    palette = plt.cm.Set2(np.linspace(0, 1, max(len(alter_components), 1)))
    component_colors = {}

    for index, component in enumerate(alter_components):
        for node in component:
            component_colors[node] = palette[index]

    pos = {EGO_ID: np.array([0.0, 0.0])}
    angles = np.linspace(0, 2 * np.pi, len(alter_components), endpoint=False)
    orbit_radius = 3.2 if len(alter_components) > 1 else 0.0

    for index, component in enumerate(alter_components):
        subgraph = alter_graph.subgraph(component)
        sub_pos = nx.spring_layout(
            subgraph,
            seed=EGO_ID + index,
            k=1.0 / np.sqrt(max(subgraph.number_of_nodes(), 1)),
        )
        raw_positions = np.array([sub_pos[node] for node in subgraph.nodes()])
        local_center = raw_positions.mean(axis=0)
        spread = np.abs(raw_positions - local_center).max()
        if spread == 0:
            spread = 1.0

        orbit_center = orbit_radius * np.array(
            [np.cos(angles[index]), np.sin(angles[index])]
        )
        local_scale = 0.7 + 0.12 * np.sqrt(subgraph.number_of_nodes())

        for node in subgraph.nodes():
            pos[node] = orbit_center + ((sub_pos[node] - local_center) / spread) * local_scale

    ego_edges = [(u, v) for u, v in G.edges() if EGO_ID in (u, v)]
    alter_edges = [(u, v) for u, v in G.edges() if EGO_ID not in (u, v)]

    fig, ax = plt.subplots(figsize=(9, 9))
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=alter_edges,
        ax=ax,
        edge_color="#B0B0B0",
        width=1.0,
        alpha=0.35,
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=ego_edges,
        ax=ax,
        edge_color="#404040",
        width=1.1,
        alpha=0.45,
    )

    alter_nodes = [node for node in G.nodes() if node != EGO_ID]
    alter_sizes = [60 + 12 * G.degree(node) for node in alter_nodes]
    alter_colors = [component_colors[node] for node in alter_nodes]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=alter_nodes,
        node_size=alter_sizes,
        node_color=alter_colors,
        edgecolors="white",
        linewidths=0.5,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[EGO_ID],
        node_size=1500,
        node_color="#D1495B",
        edgecolors="white",
        linewidths=1.5,
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels={EGO_ID: str(EGO_ID)},
        font_color="white",
        font_weight="bold",
        font_size=10,
        ax=ax,
    )

    ax.set_title("Ego node and 1-hop neighborhood\nColors show alter components without the ego")
    ax.axis("off")
    fig.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(EGO_ID, component_sizes, degree_series, mo):
    highest_alter_degree = int(degree_series.drop(EGO_ID).max())
    sizes_text = ", ".join(str(size) for size in component_sizes)
    mo.md(
        f"""
        ## Interpretation

        This local structure looks like **multiple circles**, not one single homogeneous group.
        The full graph is connected because ego **{EGO_ID}** links to every alter, but once the ego is removed the neighborhood breaks into **{len(component_sizes)}** connected pieces with sizes **{sizes_text}**.
        The degree pattern also supports that reading: the ego has degree **{int(degree_series.loc[EGO_ID])}**, the median node degree is only **{int(degree_series.median())}**, and the highest-degree alter reaches **{highest_alter_degree}**.
        Together with the visualization, that suggests one larger social cluster plus two smaller side circles that are mainly tied together through the ego.
        """
    )
    return


if __name__ == "__main__":
    app.run()
