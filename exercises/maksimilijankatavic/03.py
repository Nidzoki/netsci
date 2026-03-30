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
    # Exercise 03: Facebook Ego Network

    This notebook continues the same SNAP Facebook ego network from Exercise 02 and keeps the same ego node: **698**.

    Goal:
    compare the ego with the strongest local brokers in its neighborhood and decide whether influence is centralized or shared.

    Required input:
    `facebook/698.edges`

    Expected output:
    graph-level metrics, a top-5 centrality ranking, one broker comparison table, one annotated visualization, and a short interpretation.
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

    def resolve_data_dir():
        candidates = []

        if "__file__" in globals():
            candidates.append(Path(__file__).resolve().parent)

        cwd = Path.cwd()
        candidates.extend(
            [
                cwd,
                cwd / "exercises" / "maksimilijankatavic",
            ]
        )

        for candidate in candidates:
            data_dir = candidate / "facebook"
            if data_dir.exists():
                return candidate, data_dir

        raise FileNotFoundError(
            "Could not find the facebook dataset directory relative to the notebook "
            "or repository root."
        )

    NOTEBOOK_DIR, DATA_DIR = resolve_data_dir()
    EDGE_PATH = DATA_DIR / f"{EGO_ID}.edges"
    CIRCLE_PATH = DATA_DIR / f"{EGO_ID}.circles"

    if not EDGE_PATH.exists():
        raise FileNotFoundError(f"Could not find ego-network edge list at {EDGE_PATH}")
    return CIRCLE_PATH, EDGE_PATH, EGO_ID


@app.cell
def _(nx):
    def load_ego_network(edge_path, ego_id):
        graph = nx.read_edgelist(edge_path, nodetype=int, create_using=nx.Graph())
        alters = sorted(graph.nodes())
        graph.add_node(ego_id)
        graph.add_edges_from((ego_id, alter) for alter in alters)
        return graph
    return (load_ego_network,)


@app.cell
def _(CIRCLE_PATH, EDGE_PATH, EGO_ID, load_ego_network, nx):
    G = load_ego_network(EDGE_PATH, EGO_ID)

    circle_count = 0
    if CIRCLE_PATH.exists():
        with CIRCLE_PATH.open() as file:
            for line in file:
                if line.strip():
                    circle_count += 1

    _alter_nodes = sorted(node for node in G.nodes() if node != EGO_ID)
    alter_graph = nx.subgraph(G, _alter_nodes).copy()
    alter_components = sorted(
        nx.connected_components(alter_graph),
        key=len,
        reverse=True,
    )
    component_sizes = [len(component) for component in alter_components]

    component_lookup = {}
    for _component_index, _component_nodes in enumerate(alter_components, start=1):
        for _component_node in _component_nodes:
            component_lookup[_component_node] = _component_index
    return (
        G,
        alter_components,
        alter_graph,
        circle_count,
        component_lookup,
        component_sizes,
    )


@app.cell
def _(EGO_ID, G, alter_components, component_lookup, nx, pd):
    degree = dict(G.degree())
    degree_centrality = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)
    eigenvector = nx.eigenvector_centrality(G, max_iter=5000)

    centrality_df = pd.DataFrame(
        [
            {
                "node": node,
                "role": "ego" if node == EGO_ID else "alter",
                "alter component": "ego" if node == EGO_ID else component_lookup[node],
                "degree": degree[node],
                "degree centrality": degree_centrality[node],
                "betweenness": betweenness[node],
                "closeness": closeness[node],
                "eigenvector": eigenvector[node],
            }
            for node in G.nodes()
        ]
    ).sort_values(["betweenness", "degree"], ascending=False)

    centrality_df["betweenness rank"] = (
        centrality_df["betweenness"].rank(method="min", ascending=False).astype(int)
    )
    centrality_df["degree rank"] = (
        centrality_df["degree"].rank(method="min", ascending=False).astype(int)
    )

    top5_betweenness_df = (
        centrality_df.loc[
            :,
            [
                "node",
                "role",
                "alter component",
                "degree",
                "betweenness",
                "closeness",
                "eigenvector",
            ],
        ]
        .head(5)
        .reset_index(drop=True)
    )

    component_betweenness = {}
    local_broker_rows = []

    for _component_index, _component_nodes in enumerate(alter_components, start=1):
        _component_subgraph = G.subgraph(_component_nodes).copy()
        local_scores = nx.betweenness_centrality(_component_subgraph)
        component_betweenness[_component_index] = local_scores

        broker_node, broker_score = max(
            local_scores.items(),
            key=lambda item: (item[1], degree[item[0]], -item[0]),
        )
        local_broker_rows.append(
            {
                "alter component": _component_index,
                "component size": _component_subgraph.number_of_nodes(),
                "local broker": broker_node,
                "degree": degree[broker_node],
                "global betweenness": betweenness[broker_node],
                "local betweenness": broker_score,
            }
        )

    local_broker_df = pd.DataFrame(local_broker_rows)
    local_broker_nodes = local_broker_df["local broker"].tolist()

    comparison_rows = [
        {
            "node": EGO_ID,
            "role": "ego",
            "degree": degree[EGO_ID],
            "global betweenness": betweenness[EGO_ID],
            "share of ego betweenness": 1.0,
        }
    ]

    for _broker_row in local_broker_rows:
        _broker_node = _broker_row["local broker"]
        comparison_rows.append(
            {
                "node": _broker_node,
                "role": f"broker in component {_broker_row['alter component']}",
                "degree": degree[_broker_node],
                "global betweenness": betweenness[_broker_node],
                "share of ego betweenness": betweenness[_broker_node] / betweenness[EGO_ID],
            }
        )

    broker_comparison_df = pd.DataFrame(comparison_rows)

    removal_rows = []
    for _removed_node in [EGO_ID, *local_broker_nodes]:
        reduced_graph = G.copy()
        reduced_graph.remove_node(_removed_node)
        components_after_removal = sorted(
            (len(_component_after_removal) for _component_after_removal in nx.connected_components(reduced_graph)),
            reverse=True,
        )
        removal_rows.append(
            {
                "node": _removed_node,
                "components after removal": len(components_after_removal),
                "largest component size": components_after_removal[0],
                "component sizes": ", ".join(str(size) for size in components_after_removal),
            }
        )

    removal_impact_df = pd.DataFrame(removal_rows)

    ego_betweenness_share = betweenness[EGO_ID] / sum(betweenness.values())
    strongest_alter = (
        centrality_df.query("node != @EGO_ID")
        .sort_values(["betweenness", "degree"], ascending=False)
        .iloc[0]
    )
    ego_to_strongest_alter_ratio = betweenness[EGO_ID] / strongest_alter["betweenness"]
    return (
        betweenness,
        broker_comparison_df,
        degree,
        ego_betweenness_share,
        ego_to_strongest_alter_ratio,
        local_broker_df,
        local_broker_nodes,
        removal_impact_df,
        strongest_alter,
        top5_betweenness_df,
    )


@app.cell
def _(G, circle_count, component_sizes, ego_betweenness_share, nx, pd):
    path_scope = "full graph" if nx.is_connected(G) else "largest connected component"
    path_graph = G if nx.is_connected(G) else G.subgraph(max(nx.connected_components(G), key=len)).copy()

    metrics_rows = [
        {"metric": "nodes", "value": G.number_of_nodes()},
        {"metric": "edges", "value": G.number_of_edges()},
        {"metric": "density", "value": round(nx.density(G), 4)},
        {"metric": "average clustering", "value": round(nx.average_clustering(G), 4)},
        {"metric": "average shortest path scope", "value": path_scope},
        {
            "metric": "average shortest path length",
            "value": round(nx.average_shortest_path_length(path_graph), 4),
        },
        {"metric": "annotated circles in SNAP file", "value": circle_count},
        {"metric": "alter components without ego", "value": len(component_sizes)},
        {"metric": "alter component sizes", "value": ", ".join(str(size) for size in component_sizes)},
        {"metric": "ego share of total betweenness", "value": round(ego_betweenness_share, 4)},
    ]

    metrics_df = pd.DataFrame(metrics_rows)
    return (metrics_df,)


@app.cell(hide_code=True)
def _(
    EGO_ID,
    G,
    component_sizes,
    ego_betweenness_share,
    ego_to_strongest_alter_ratio,
    mo,
    strongest_alter,
):
    sizes_text = ", ".join(str(size) for size in component_sizes)
    mo.md(
        f"""
        The ego network for **{EGO_ID}** has **{G.number_of_nodes()} nodes** and **{G.number_of_edges()} edges**.
        The full graph is connected, but removing the ego splits the alters into **{len(component_sizes)}** components of sizes **{sizes_text}**.

        Brokerage is highly concentrated:
        the ego captures **{ego_betweenness_share:.1%}** of all betweenness in the neighborhood, and its betweenness is **{ego_to_strongest_alter_ratio:.1f}x** larger than the strongest alter broker (**node {int(strongest_alter['node'])}**).
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Graph-Level Metrics
    """)
    return


@app.cell
def _(metrics_df):
    metrics_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Top 5 Nodes by Betweenness
    """)
    return


@app.cell
def _(top5_betweenness_df):
    top5_betweenness_df.round(
        {
            "betweenness": 4,
            "closeness": 4,
            "eigenvector": 4,
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Ego vs Strongest Local Brokers

    The table below compares the ego to the strongest broker inside each alter component after the ego is removed.
    """)
    return


@app.cell
def _(broker_comparison_df, local_broker_df, removal_impact_df):
    comparison_df = broker_comparison_df.merge(
        local_broker_df,
        how="left",
        left_on="node",
        right_on="local broker",
    ).merge(removal_impact_df, how="left", on="node")

    comparison_df = comparison_df.loc[
        :,
        [
            "node",
            "role",
            "degree_x",
            "global betweenness_x",
            "share of ego betweenness",
            "component size",
            "local betweenness",
            "components after removal",
            "component sizes",
        ],
    ].rename(
        columns={
            "degree_x": "degree",
            "global betweenness_x": "global betweenness",
        }
    )

    comparison_df.round(
        {
            "global betweenness": 4,
            "share of ego betweenness": 3,
            "local betweenness": 4,
        }
    )
    return (comparison_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    `local betweenness` is computed inside each alter component only.
    That makes it useful for spotting backup brokers inside circles, even when their global reach stays small.
    """)
    return


@app.cell
def _(comparison_df):
    comparison_df.round(
        {
            "global betweenness": 4,
            "share of ego betweenness": 3,
            "local betweenness": 4,
        }
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Annotated Visualization
    """)
    return


@app.cell
def _(
    EGO_ID,
    G,
    alter_components,
    alter_graph,
    betweenness,
    degree,
    local_broker_nodes,
    np,
    nx,
    plt,
):
    palette = plt.cm.Set2(np.linspace(0, 1, max(len(alter_components), 1)))
    component_colors = {}

    for _layout_index, _layout_component in enumerate(alter_components):
        for _layout_node in _layout_component:
            component_colors[_layout_node] = palette[_layout_index]

    pos = {EGO_ID: np.array([0.0, 0.0])}
    angles = np.linspace(0, 2 * np.pi, len(alter_components), endpoint=False)
    orbit_radius = 3.4 if len(alter_components) > 1 else 0.0

    for _layout_index, _layout_component in enumerate(alter_components):
        _layout_subgraph = alter_graph.subgraph(_layout_component)
        sub_pos = nx.spring_layout(
            _layout_subgraph,
            seed=EGO_ID + _layout_index,
            k=1.0 / np.sqrt(max(_layout_subgraph.number_of_nodes(), 1)),
        )
        raw_positions = np.array([sub_pos[_layout_node] for _layout_node in _layout_subgraph.nodes()])
        local_center = raw_positions.mean(axis=0)
        spread = np.abs(raw_positions - local_center).max()
        if spread == 0:
            spread = 1.0

        orbit_center = orbit_radius * np.array(
            [np.cos(angles[_layout_index]), np.sin(angles[_layout_index])]
        )
        local_scale = 0.75 + 0.12 * np.sqrt(_layout_subgraph.number_of_nodes())

        for _layout_node in _layout_subgraph.nodes():
            pos[_layout_node] = orbit_center + ((sub_pos[_layout_node] - local_center) / spread) * local_scale

    ego_edges = [(u, v) for u, v in G.edges() if EGO_ID in (u, v)]
    alter_edges = [(u, v) for u, v in G.edges() if EGO_ID not in (u, v)]

    fig, ax = plt.subplots(figsize=(9, 9))
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=alter_edges,
        ax=ax,
        edge_color="#B5B5B5",
        width=1.0,
        alpha=0.35,
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=ego_edges,
        ax=ax,
        edge_color="#505050",
        width=1.0,
        alpha=0.30,
    )

    _plot_alter_nodes = [node for node in G.nodes() if node != EGO_ID]
    alter_sizes = [120 + 3800 * betweenness[node] + 8 * degree[node] for node in _plot_alter_nodes]
    alter_colors = [component_colors[node] for node in _plot_alter_nodes]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=_plot_alter_nodes,
        node_size=alter_sizes,
        node_color=alter_colors,
        edgecolors="white",
        linewidths=0.6,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=local_broker_nodes,
        node_size=[120 + 3800 * betweenness[node] + 8 * degree[node] for node in local_broker_nodes],
        node_color=[component_colors[node] for node in local_broker_nodes],
        edgecolors="#1A1A1A",
        linewidths=2.0,
        ax=ax,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[EGO_ID],
        node_size=3200,
        node_color="#D1495B",
        edgecolors="white",
        linewidths=1.5,
        ax=ax,
    )

    labels = {EGO_ID: str(EGO_ID), **{node: str(node) for node in local_broker_nodes}}
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=10,
        font_weight="bold",
        font_color="#1A1A1A",
        ax=ax,
    )

    ax.text(
        0.02,
        0.02,
        "Node size = global betweenness\nBlack outlines = strongest broker in each alter component",
        transform=ax.transAxes,
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#D0D0D0"},
    )
    ax.set_title(
        "Ego 698 and its strongest local brokers\nColors show alter components after removing the ego"
    )
    ax.axis("off")
    fig.tight_layout()
    fig
    return


@app.cell(hide_code=True)
def _(EGO_ID, comparison_df, mo, strongest_alter):
    ego_row = comparison_df.loc[comparison_df["node"] == EGO_ID].iloc[0]
    strongest_local_rows = comparison_df.loc[comparison_df["node"] != EGO_ID]

    local_broker_text = ", ".join(
        f"{int(row['node'])} (component {row['role'].split()[-1]})"
        for _, row in strongest_local_rows.iterrows()
    )

    mo.md(
        f"""
        ## Interpretation

        The neighborhood is best described as **centralized around the ego**, not as influence that is evenly shared across several brokers.

        The strongest evidence is structural:
        ego **{EGO_ID}** has global betweenness **{ego_row['global betweenness']:.4f}**, while the strongest alter overall is **{int(strongest_alter['node'])}** with only **{strongest_alter['betweenness']:.4f}**.
        Removing the ego splits the network into several pieces, but removing the strongest local brokers does **not** disconnect the full neighborhood.

        Influence is still **partly shared inside components**.
        The main backup brokers are **{local_broker_text}**.
        Their local betweenness scores show they help organize traffic inside their own circles, but their global reach remains much smaller than the ego's.

        Degree and betweenness therefore do not mean exactly the same thing here:
        some nodes are popular because they connect to many neighbors, while brokerage is concentrated on nodes that sit between local groups.
        In this ego network, the ego does both.
        """
    )
    return


if __name__ == "__main__":
    app.run()
