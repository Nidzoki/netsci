# lectures/10/generate_images.py

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
from scipy.integrate import odeint
import matplotlib.patches as mpatches

# Create images directory next to this script so it works from any cwd.
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(output_dir, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid') # Using a seaborn style for nicer plots

# --- 1. Independent Cascade Model Steps ---
def plot_independent_cascade():
    print("Generating independent_cascade_steps.png...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) # Increased figure size
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('A', 'X'), ('B', 'C'), ('B', 'D'), ('X','Y')])
    # Adjusted positions for better clarity and less overlap
    pos = {'A': (0, 1), 'B': (1.5, 1.5), 'C': (3, 2), 'D': (3, 1), 'X':(1.5,0.5), 'Y':(3,0)}

    node_opts = {"node_size": 2500, "font_size":12, "font_weight":"bold"}
    edge_opts = {"arrowsize": 25, "width": 2.5}

    # Step 1
    ax = axes[0]
    node_colors_s1 = {'A': 'salmon', 'B': 'skyblue', 'C': 'skyblue', 'D': 'skyblue', 'X': 'skyblue', 'Y': 'skyblue'}
    edge_colors_s1 = {('A','B'):'red', ('A','X'):'dimgray', ('B','C'):'dimgray', ('B','D'):'dimgray', ('X','Y'):'dimgray'}
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=[node_colors_s1.get(n) for n in G.nodes()],
            edge_color=[edge_colors_s1.get(e, edge_colors_s1.get((e[1],e[0]),'dimgray')) for e in G.edges()],
            labels={n:n for n in G.nodes()}, **node_opts, **edge_opts)
    ax.set_title("Step 1: A activates B (prob p1)", fontsize=14)

    # Step 2
    ax = axes[1]
    node_colors_s2 = {'A': 'lightgray', 'B': 'salmon', 'C': 'skyblue', 'D': 'skyblue', 'X': 'skyblue', 'Y': 'skyblue'}
    edge_colors_s2 = {('A','B'):'lightgray', ('A','X'):'lightgray', ('B','C'):'red', ('B','D'):'red', ('X','Y'):'dimgray'}
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=[node_colors_s2.get(n) for n in G.nodes()],
            edge_color=[edge_colors_s2.get(e, edge_colors_s2.get((e[1],e[0]),'dimgray')) for e in G.edges()],
            labels={n:n for n in G.nodes()}, **node_opts, **edge_opts)
    ax.set_title("Step 2: B attempts C (p2) & D (p3)", fontsize=14)

    # Step 3
    ax = axes[2]
    node_colors_s3 = {'A': 'lightgray', 'B': 'lightgray', 'C': 'salmon', 'D': '#E0E0E0', 'X':'skyblue', 'Y': 'skyblue'} # D fails (lighter gray)
    edge_colors_s3 = {('A','B'):'lightgray', ('A','X'):'lightgray', ('B','C'):'lightgray', ('B','D'):'lightgray', ('X','Y'):'dimgray'}
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=[node_colors_s3.get(n) for n in G.nodes()],
            edge_color=[edge_colors_s3.get(e, edge_colors_s3.get((e[1],e[0]),'dimgray')) for e in G.edges()],
            labels={n:n for n in G.nodes()}, **node_opts, **edge_opts)
    ax.text(pos['D'][0], pos['D'][1]-0.25, "Failed", ha='center', va='top', color='darkred', fontsize=12, weight='bold')
    ax.set_title("Step 3: C activates, D fails", fontsize=14)

    for ax_i in axes: ax_i.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "independent_cascade_steps.png"), dpi=120)
    plt.close()

# --- 2. Linear Threshold Model Steps ---
def plot_linear_threshold():
    print("Generating linear_threshold_steps.png...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 7)) # Increased figure size
    G = nx.DiGraph()
    G.add_edges_from([('A', 'X'), ('B', 'X'), ('C', 'X')])
    pos = {'A': (0, 2), 'B': (0, 1), 'C': (0, 0), 'X': (1.5, 1)} # X further
    threshold_X = 0.6
    weights = {('A', 'X'): 0.3, ('B', 'X'): 0.4, ('C', 'X'): 0.2}

    node_opts = {"node_size": 3500, "font_size":14, "font_weight":"bold"}
    edge_opts = {"arrowsize": 30, "width": 2.5}

    # Step 1
    ax = axes[0]
    node_colors_s1 = {'A': 'salmon', 'B': 'salmon', 'C': 'skyblue', 'X': 'skyblue'}
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=[node_colors_s1.get(n) for n in G.nodes()],
            labels={n:n for n in G.nodes()}, **node_opts, **edge_opts)
    edge_labels = {k: f"w={v}" for k, v in weights.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=12, font_color='black')
    current_influence_s1 = weights[('A','X')] + weights[('B','X')]
    ax.text(pos['X'][0], pos['X'][1] + 0.3, f"Node X\nθ$_X$ = {threshold_X}\nΣw_active = {current_influence_s1:.1f}",
            ha='center', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.7, boxstyle="round,pad=0.3"))
    ax.set_title(f"Step 1: A, B active. Σw ({current_influence_s1:.1f}) < θ$_X$ ({threshold_X}). X inactive.", fontsize=14)

    # Step 2 (C becomes active too, now X activates)
    ax = axes[1]
    node_colors_s2 = {'A': 'salmon', 'B': 'salmon', 'C': 'salmon', 'X': 'salmon'} # X activates
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=[node_colors_s2.get(n) for n in G.nodes()],
            labels={n:n for n in G.nodes()}, **node_opts, **edge_opts)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=12, font_color='black')
    sum_w_active_s2 = weights[('A','X')] + weights[('B','X')] + weights[('C','X')]
    ax.text(pos['X'][0], pos['X'][1] + 0.3, f"Node X\nθ$_X$ = {threshold_X}\nΣw_active = {sum_w_active_s2:.1f}",
            ha='center', va='bottom', fontsize=12, bbox=dict(facecolor='white', alpha=0.7, boxstyle="round,pad=0.3"))
    ax.set_title(f"Step 2: A, B, C active. Σw ({sum_w_active_s2:.1f}) ≥ θ$_X$ ({threshold_X}). X activates.", fontsize=14)

    for ax_i in axes: ax_i.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "linear_threshold_steps.png"), dpi=120)
    plt.close()

# --- 3. SIS Model ---
def plot_sis_model():
    print("Generating sis_model.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) # Increased figure size

    # State Diagram
    ax1.text(0.25, 0.5, "S", fontsize=24, ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.6", fc="skyblue", ec="black"))
    ax1.text(0.75, 0.5, "I", fontsize=24, ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.6", fc="salmon", ec="black"))
    ax1.annotate("", xy=(0.65, 0.55), xytext=(0.35, 0.55), arrowprops=dict(arrowstyle="->", lw=2.5, color="black"))
    ax1.text(0.5, 0.62, r"$\beta \frac{S \cdot I}{N}$", ha='center', va='bottom', fontsize=16)
    ax1.annotate("", xy=(0.35, 0.45), xytext=(0.65, 0.45), arrowprops=dict(arrowstyle="->", lw=2.5, color="black"))
    ax1.text(0.5, 0.38, r"$\gamma I$", ha='center', va='top', fontsize=16)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.set_title("SIS State Transitions", fontsize=14)

    # Conceptual Plot
    def sis_odes(y, t, N, beta, gamma):
        S, I = y
        dSdt = -beta * S * I / N + gamma * I
        dIdt = beta * S * I / N - gamma * I
        return dSdt, dIdt

    N = 1000
    I0 = 10 # Start with a few infected
    S0 = N - I0
    y0 = S0, I0
    t = np.linspace(0, 100, 200)
    beta = 0.3
    gamma = 0.1 # R0_effective = beta/gamma = 3

    sol = odeint(sis_odes, y0, t, args=(N, beta, gamma))
    S, I = sol.T

    ax2.plot(t, S/N, 'b-', label='Susceptible (S/N)', linewidth=2)
    ax2.plot(t, I/N, 'r-', label='Infected (I/N)', linewidth=2)
    ax2.set_xlabel("Time", fontsize=12)
    ax2.set_ylabel("Fraction of Population", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.set_title(r"SIS Model Dynamics ($\beta=0.3, \gamma=0.1$)", fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.tick_params(labelsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sis_model.png"), dpi=120)
    plt.close()

# --- 4. SIR Model ---
def plot_sir_model():
    print("Generating sir_model.png...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6)) # Increased figure size

    # State Diagram
    ax1.text(0.15, 0.5, "S", fontsize=24, ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.6", fc="skyblue", ec="black"))
    ax1.text(0.5, 0.5, "I", fontsize=24, ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.6", fc="salmon", ec="black"))
    ax1.text(0.85, 0.5, "R", fontsize=24, ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.6", fc="lightgreen", ec="black"))
    ax1.annotate("", xy=(0.4, 0.5), xytext=(0.25, 0.5), arrowprops=dict(arrowstyle="->", lw=2.5, color="black"))
    ax1.text(0.325, 0.58, r"$\beta \frac{S \cdot I}{N}$", ha='center', va='bottom', fontsize=16)
    ax1.annotate("", xy=(0.75, 0.5), xytext=(0.6, 0.5), arrowprops=dict(arrowstyle="->", lw=2.5, color="black"))
    ax1.text(0.675, 0.58, r"$\gamma I$", ha='center', va='bottom', fontsize=16)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.set_title("SIR State Transitions", fontsize=14)

    # Conceptual Plot
    def sir_odes(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    N = 1000
    I0, R0_val = 1, 0 # Start with 1 infected, 0 recovered
    S0 = N - I0 - R0_val
    y0 = S0, I0, R0_val
    t = np.linspace(0, 160, 300)
    beta = 0.2
    gamma = 0.1 # R0 = beta/gamma = 2

    sol = odeint(sir_odes, y0, t, args=(N, beta, gamma))
    S, I, R = sol.T

    ax2.plot(t, S/N, 'b-', label='Susceptible (S/N)', linewidth=2)
    ax2.plot(t, I/N, 'r-', label='Infected (I/N)', linewidth=2)
    ax2.plot(t, R/N, 'g-', label='Recovered (R/N)', linewidth=2)
    ax2.set_xlabel("Time", fontsize=12)
    ax2.set_ylabel("Fraction of Population", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.set_title(r"SIR Model Dynamics ($\beta=0.2, \gamma=0.1$)", fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.tick_params(labelsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sir_model.png"), dpi=120)
    plt.close()

# --- 5. Voter Model Evolution ---
def plot_voter_model():
    print("Generating voter_model_evolution.png...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) # Increased figure size
    G = nx.random_geometric_graph(25, 0.35, seed=42) # Slightly larger graph
    pos = nx.spring_layout(G, seed=42, k=0.5)

    opinions = [-1, 1] # Two opinions: Blue and Red
    node_opts = {"node_size": 600, "font_size": 0} # No labels for clarity
    edge_opts = {"width": 1.5, "edge_color":"gray"}

    # Step 1: Initial random opinions
    np.random.seed(42) # for reproducibility of opinions
    current_opinions_s1 = {node: np.random.choice(opinions) for node in G.nodes()}
    colors_s1 = ['cornflowerblue' if current_opinions_s1[n] == -1 else 'salmon' for n in G.nodes()]
    nx.draw(G, pos, ax=axes[0], node_color=colors_s1, **node_opts, **edge_opts)
    axes[0].set_title("Step 1: Initial Random Opinions", fontsize=14)

    # Simulate a few steps for intermediate state
    current_opinions_s2 = current_opinions_s1.copy()
    for _ in range(int(G.number_of_nodes() * 2)): # Few iterations relative to N
        node_to_update = np.random.choice(list(G.nodes()))
        if list(G.neighbors(node_to_update)):
            neighbor = np.random.choice(list(G.neighbors(node_to_update)))
            current_opinions_s2[node_to_update] = current_opinions_s2[neighbor]

    colors_s2 = ['cornflowerblue' if current_opinions_s2[n] == -1 else 'salmon' for n in G.nodes()]
    nx.draw(G, pos, ax=axes[1], node_color=colors_s2, **node_opts, **edge_opts)
    axes[1].set_title("Step 2: Opinion Domains Form", fontsize=14)

    # Simulate many steps for final state (likely consensus)
    current_opinions_s3 = current_opinions_s2.copy()
    for _ in range(int(G.number_of_nodes() * 20)): # More iterations
        node_to_update = np.random.choice(list(G.nodes()))
        if list(G.neighbors(node_to_update)):
            neighbor = np.random.choice(list(G.neighbors(node_to_update)))
            current_opinions_s3[node_to_update] = current_opinions_s3[neighbor]
        if len(set(current_opinions_s3.values())) == 1: # Consensus reached
            break
    colors_s3 = ['cornflowerblue' if current_opinions_s3[n] == -1 else 'salmon' for n in G.nodes()]
    nx.draw(G, pos, ax=axes[2], node_color=colors_s3, **node_opts, **edge_opts)
    axes[2].set_title("Step 3: Consensus Reached", fontsize=14)

    for ax_i in axes: ax_i.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "voter_model_evolution.png"), dpi=120)
    plt.close()

# --- 6. Bounded Confidence Model ---
def plot_bounded_confidence():
    print("Generating bounded_confidence_model.png...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True) # Increased figure size
    num_nodes = 100 # More nodes for better visualization
    np.random.seed(42)
    opinions_initial = np.random.rand(num_nodes)
    confidence_bound = 0.1 # Smaller bound for more distinct clusters
    mu = 0.3 # convergence parameter

    # Initial State
    axes[0].scatter(opinions_initial, np.random.uniform(0.4, 0.6, num_nodes), alpha=0.7, s=80, c='cornflowerblue', edgecolors='w')
    axes[0].set_xlim(-0.05, 1.05)
    axes[0].set_ylim(0, 1)
    axes[0].set_yticks([])
    axes[0].set_xlabel("Opinion Value", fontsize=12)
    axes[0].set_title("Initial Random Opinion Distribution", fontsize=14)
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Simulate for final state
    opinions_final = opinions_initial.copy()
    for _ in range(num_nodes * 100): # More Iterations
        i = np.random.randint(num_nodes)
        j = np.random.randint(num_nodes)
        if i == j:
            continue
        if abs(opinions_final[i] - opinions_final[j]) < confidence_bound:
            op_i_old = opinions_final[i] # Store old value before it's updated
            opinions_final[i] += mu * (opinions_final[j] - opinions_final[i])
            opinions_final[j] += mu * (op_i_old - opinions_final[j])


    axes[1].scatter(opinions_final, np.random.uniform(0.4, 0.6, num_nodes), alpha=0.7, s=80, c='salmon', edgecolors='w')
    axes[1].set_xlim(-0.05, 1.05)
    axes[1].set_xlabel("Opinion Value", fontsize=12)
    axes[1].set_title(f"Final State (Clusters Form, ε={confidence_bound})", fontsize=14)
    axes[1].grid(True, linestyle='--', alpha=0.5)
    axes[1].tick_params(labelsize=10)
    axes[0].tick_params(labelsize=10)


    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bounded_confidence_model.png"), dpi=120)
    plt.close()

# --- 7. Sandpile Model Conceptual ---
def plot_sandpile_model():
    print("Generating sandpile_model.png...")
    grid_size = 5
    threshold = 4
    np.random.seed(42)
    grid_s1 = np.random.randint(0, threshold, size=(grid_size, grid_size))

    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) # Increased figure size

    def plot_grid(ax, current_grid, title, highlight_cells=None):
        ax.imshow(current_grid, cmap='viridis_r', vmin=0, vmax=threshold + 2, interpolation='nearest')
        for i in range(grid_size):
            for j in range(grid_size):
                val = current_grid[i, j]
                color = "black" if val < threshold -1 else "white"
                ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=12, weight="bold")
                if highlight_cells and (i,j) in highlight_cells:
                    rect = mpatches.Rectangle((j-0.5, i-0.5), 1, 1, linewidth=3, edgecolor='red', facecolor='none')
                    ax.add_patch(rect)
        ax.set_title(title, fontsize=14)
        ax.set_xticks([])
        ax.set_yticks([])

    # Initial State
    plot_grid(axes[0], grid_s1, "Initial State")

    # Add sand to a cell to trigger topple
    grid_s2 = grid_s1.copy()
    center_i, center_j = grid_size // 2, grid_size // 2
    grid_s2[center_i, center_j] += 3 # Make it likely to topple
    plot_grid(axes[1], grid_s2, f"Adding Sand (Cell ({center_i},{center_j}) at {grid_s2[center_i,center_j]})", highlight_cells=[(center_i, center_j)])

    # Simulate one topple (conceptual)
    grid_s3 = grid_s2.copy()
    toppled_cells = []
    if grid_s3[center_i, center_j] >= threshold:
        grid_s3[center_i, center_j] -= threshold
        toppled_cells.append((center_i, center_j))
        neighbors_to_update = []
        if center_i > 0: grid_s3[center_i - 1, center_j] += 1; neighbors_to_update.append((center_i-1, center_j))
        if center_i < grid_size - 1: grid_s3[center_i + 1, center_j] += 1; neighbors_to_update.append((center_i+1, center_j))
        if center_j > 0: grid_s3[center_i, center_j - 1] += 1; neighbors_to_update.append((center_i, center_j-1))
        if center_j < grid_size - 1: grid_s3[center_i, center_j + 1] += 1; neighbors_to_update.append((center_i, center_j+1))
        # Second order topple for illustration if any neighbor also topples
        for ni, nj in neighbors_to_update:
            if grid_s3[ni,nj] >= threshold:
                grid_s3[ni,nj] -= threshold
                toppled_cells.append((ni,nj))
                if ni > 0 and (ni-1, nj) not in toppled_cells : grid_s3[ni - 1, nj] += 1
                if ni < grid_size - 1 and (ni+1,nj) not in toppled_cells: grid_s3[ni + 1, nj] += 1
                if nj > 0 and (ni,nj-1) not in toppled_cells: grid_s3[ni, nj - 1] += 1
                if nj < grid_size - 1 and (ni,nj+1) not in toppled_cells: grid_s3[ni, nj + 1] += 1


    plot_grid(axes[2], grid_s3, "After Topples & Local Spread", highlight_cells=toppled_cells)


    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sandpile_model.png"), dpi=120)
    plt.close()


if __name__ == "__main__":
    plot_independent_cascade()
    plot_linear_threshold()
    plot_sis_model()
    plot_sir_model()
    plot_voter_model()
    plot_bounded_confidence()
    plot_sandpile_model()
    print(f"All images generated in {output_dir}")
