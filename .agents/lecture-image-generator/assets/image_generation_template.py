#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lecture Image Generation Template
================================

This template provides a standardized structure for creating images
to support lecture slides. Customize this file for specific lecture needs.

Required packages:
- networkx>=2.6
- matplotlib>=3.4
- numpy>=1.20
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Optional, List, Tuple, Dict, Any, Union

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Global style settings
plt.style.use('ggplot')
COLORS = {
    'primary': 'skyblue',
    'secondary': 'lightgreen',
    'accent': 'salmon',
    'highlight': 'red',
    'neutral': 'gray'
}

def save_figure(
    fig_obj: Any,
    filename: str,
    title: Optional[str] = None,
    pos: Optional[Dict] = None,
    node_color: Union[str, List] = COLORS['primary'],
    edge_color: Union[str, List] = COLORS['neutral'],
    node_size: Union[int, List] = 300,
    width: Union[float, List] = 1.0,
    with_labels: bool = True,
    font_size: int = 10,
    figsize: Tuple[int, int] = (10, 8),
    dpi: int = 100,
    **kwargs
) -> None:
    """
    Save a figure with consistent styling.

    Parameters
    ----------
    fig_obj : networkx.Graph or matplotlib.figure.Figure
        The graph or figure object to visualize
    filename : str
        The filename to save the image as (without path)
    title : str, optional
        Title to display on the figure
    pos : dict, optional
        Node positions for network visualizations
    node_color : str or list, optional
        Color(s) for nodes
    edge_color : str or list, optional
        Color(s) for edges
    node_size : int or list, optional
        Size(s) for nodes
    width : float or list, optional
        Width(s) for edges
    with_labels : bool, optional
        Whether to display node labels
    font_size : int, optional
        Size of font for labels
    figsize : tuple, optional
        Figure dimensions (width, height) in inches
    dpi : int, optional
        Resolution in dots per inch
    **kwargs : dict
        Additional keyword arguments passed to drawing functions
    """
    # Check if fig_obj is already a matplotlib figure
    if isinstance(fig_obj, plt.Figure):
        fig = fig_obj
    else:
        # Create a new figure
        fig = plt.figure(figsize=figsize)

        # If it's a networkx graph, draw it
        if isinstance(fig_obj, nx.Graph) or isinstance(fig_obj, nx.DiGraph):
            G = fig_obj

            # Generate positions if not provided
            if pos is None:
                pos = nx.spring_layout(G, seed=42)

            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=node_size)

            # Draw edges, with arrows if directed
            if isinstance(G, nx.DiGraph):
                nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=width,
                                       arrowsize=15, **kwargs)
            else:
                nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=width, **kwargs)

            # Draw labels if requested
            if with_labels:
                nx.draw_networkx_labels(G, pos, font_size=font_size)

    # Add title if provided
    if title:
        plt.title(title, fontsize=16)

    # Final styling
    plt.axis('off')
    plt.tight_layout()

    # Save and close
    plt.savefig(f'images/{filename}', dpi=dpi, bbox_inches='tight')
    plt.close()
    print(f"Saved {filename}")

def generate_basic_graph() -> nx.Graph:
    """
    Generate a basic graph visualization as an example.

    Returns
    -------
    networkx.Graph
        The generated graph
    """
    print("Generating basic graph...")

    # Create a simple graph
    G = nx.Graph()
    G.add_edges_from([
        (1, 2), (1, 3), (2, 3), (3, 4), (4, 5),
        (5, 6), (6, 7), (7, 8), (8, 5)
    ])

    # Generate positions
    pos = nx.spring_layout(G, seed=42)

    # Save the visualization
    save_figure(G, 'basic_graph.png', pos=pos,
                title='Basic Graph Example', with_labels=True)

    return G

def generate_highlighted_features(G: Optional[nx.Graph] = None) -> nx.Graph:
    """
    Generate a graph with highlighted features.

    Parameters
    ----------
    G : networkx.Graph, optional
        An existing graph to use, or None to create a new one

    Returns
    -------
    networkx.Graph
        The graph with highlighted features
    """
    print("Generating graph with highlighted features...")

    # Create a graph if none is provided
    if G is None:
        G = nx.Graph()
        G.add_edges_from([
            (1, 2), (1, 3), (2, 3), (3, 4), (4, 5),
            (5, 6), (6, 7), (7, 8), (8, 5)
        ])

    # Generate positions
    pos = nx.spring_layout(G, seed=42)

    # Find features to highlight (example: high-degree nodes)
    node_colors = []
    for node in G.nodes():
        if G.degree(node) > 2:
            node_colors.append(COLORS['highlight'])
        else:
            node_colors.append(COLORS['primary'])

    # Save the visualization
    save_figure(G, 'highlighted_graph.png', pos=pos,
                node_color=node_colors,
                title='Graph with Highlighted Features')

    return G

def generate_custom_matplotlib_figure() -> None:
    """
    Generate a custom matplotlib figure not based on a network.
    """
    print("Generating custom matplotlib figure...")

    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate some data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Plot the data
    ax.plot(x, y1, 'b-', linewidth=2, label='Sin(x)')
    ax.plot(x, y2, 'r-', linewidth=2, label='Cos(x)')

    # Add labels and title
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_title('Custom Plot Example')
    ax.legend()
    ax.grid(True)

    # Save the figure
    save_figure(fig, 'custom_plot.png', dpi=120)

def main() -> None:
    """
    Main function to generate all required images.
    """
    print("Starting image generation...")

    # Generate basic graph
    G = generate_basic_graph()

    # Generate highlighted features using the same graph
    generate_highlighted_features(G)

    # Generate custom matplotlib figure
    generate_custom_matplotlib_figure()

    print("Image generation complete!")

if __name__ == "__main__":
    main()