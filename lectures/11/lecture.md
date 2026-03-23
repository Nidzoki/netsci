---
marp: true
theme: default
paginate: true
footer: 'Network Analysis - PMF-UNIST 2025/2026'

<style>
section pre code {
  font-size: 0.75em;
}
section.small-code pre code {
  font-size: 0.65em;
}
</style>
---

# Case Study: Character Network Analysis
## From Screenplay to Social Network - "Conclave" (2024)

Network Analysis - Lecture 11
Nikola Balic, Faculty of Natural Science, University of Split
Data Science and Engineering Master Program

---

## Today's Objective

**Build a character relationship network from a movie screenplay using Python**

- **Data Source:** "Conclave" (2024) screenplay PDF
- **Tools:** Google Colab, NetworkX, spaCy, Claude API
- **Goal:** Extract, analyze, and visualize character relationships
- **Skills:** Text processing, NER, network construction, centrality analysis

![width:400px bg right:35%](images/example_character_network.png)

---

## What You'll Learn Today

1. **Text Processing:** Extract and clean screenplay text from PDF
2. **Named Entity Recognition (NER):** Identify character names using spaCy
3. **Relationship Extraction:** Infer connections from character proximity
4. **Network Construction:** Build graphs with NetworkX
5. **Network Analysis:** Calculate centralities and detect communities
6. **AI Enhancement:** Use Claude API for relationship type inference
7. **Visualization:** Create interactive network plots

---

## Step 1: Setting Up Google Colab

**Open a new Google Colab notebook and run:**

```python
# Install required packages
!pip install networkx matplotlib spacy anthropic plotly
!pip install PyPDF2 python-docx
!python -m spacy download en_core_web_sm

# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy
import re
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px
```

---

## Step 2: Download and Load the Screenplay

```python
# Download the Conclave screenplay
import requests
import PyPDF2
from io import BytesIO

# Download PDF from ScriptSlug
url = "https://www.scriptslug.com/script/conclave-2024"
print("Visit the URL above to download conclave-2024.pdf")
print("Then upload it to your Colab environment")

# Upload file in Colab
from google.colab import files
uploaded = files.upload()

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Load the screenplay text
screenplay_text = extract_text_from_pdf('conclave-2024.pdf')
print(f"Extracted {len(screenplay_text)} characters from screenplay")
```

---

## Step 3: Character Name Recognition

**Define the main characters and set up NER:**

```python
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define full character names from the screenplay
full_character_names = [
    "Thomas Lawrence", "Aldo Bellini", "Joseph Tremblay",
    "Joshua Adeyemi", "Raymond O'Malley", "Vincent Benitez",
    "Sabbadin", "Mandorff", "Goffredo Tedesco", "Agnes",
    "Janusz Woźniak", "Villanueva", "Lombardi", "Shanumi"
]

# Create name variations (first names, last names)
name_variations = {}
for full_name in full_character_names:
    parts = full_name.split()
    name_variations[full_name] = full_name
    for part in parts:
        if len(part) > 2:  # Avoid short words
            name_variations[part] = full_name

print(f"Created {len(name_variations)} name variations")
print("Sample variations:", list(name_variations.items())[:5])
```

---

## Step 4: Extract Character Interactions

```python
def extract_interactions(text, window_size=100):
    """Extract character interactions based on proximity in text."""
    interactions = []

    # Process text in chunks
    doc = nlp(text)

    # Find all person entities
    persons = [(ent.text, ent.start_char, ent.end_char)
               for ent in doc.ents if ent.label_ == "PERSON"]

    # Map to full character names
    mapped_persons = []
    for person, start, end in persons:
        if person in name_variations:
            mapped_persons.append((name_variations[person], start, end))

    # Find interactions within window
    for i, (char1, start1, end1) in enumerate(mapped_persons):
        for j, (char2, start2, end2) in enumerate(mapped_persons[i+1:], i+1):
            if abs(start1 - start2) <= window_size and char1 != char2:
                # Extract context
                context_start = max(0, min(start1, start2) - 50)
                context_end = min(len(text), max(end1, end2) + 50)
                context = text[context_start:context_end]

                interactions.append((char1, char2, context))

    return interactions

# Extract interactions
print("Extracting character interactions...")
interactions = extract_interactions(screenplay_text)
print(f"Found {len(interactions)} potential interactions")
```

---

## Step 5: Build the Character Network

```python
# Create NetworkX graph
G = nx.Graph()

# Add nodes (characters)
for char in full_character_names:
    G.add_node(char)

# Count interactions and add edges
interaction_counts = defaultdict(int)
for char1, char2, context in interactions:
    pair = tuple(sorted([char1, char2]))
    interaction_counts[pair] += 1

# Add edges with weights
for (char1, char2), weight in interaction_counts.items():
    if weight >= 2:  # Minimum threshold
        G.add_edge(char1, char2, weight=weight)

# Print basic network statistics
print(f"Network has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
print(f"Network density: {nx.density(G):.3f}")
print(f"Is connected: {nx.is_connected(G)}")

if not nx.is_connected(G):
    components = list(nx.connected_components(G))
    print(f"Number of connected components: {len(components)}")
    print(f"Largest component size: {len(max(components, key=len))}")
```

---

## Step 6: Network Analysis - Centrality Measures

```python
# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Create centrality DataFrame
centrality_df = pd.DataFrame({
    'Character': list(G.nodes()),
    'Degree': [degree_centrality[node] for node in G.nodes()],
    'Betweenness': [betweenness_centrality[node] for node in G.nodes()],
    'Closeness': [closeness_centrality[node] for node in G.nodes()],
    'Eigenvector': [eigenvector_centrality[node] for node in G.nodes()]
})

# Sort by degree centrality
centrality_df = centrality_df.sort_values('Degree', ascending=False)
print("Top 5 most central characters:")
print(centrality_df.head())
```

---

## Step 7: Community Detection

```python
# Detect communities using Louvain algorithm
communities = nx.community.louvain_communities(G)

print(f"Found {len(communities)} communities:")
for i, community in enumerate(communities):
    print(f"Community {i+1}: {list(community)}")

# Add community information to nodes
community_map = {}
for i, community in enumerate(communities):
    for node in community:
        community_map[node] = i

nx.set_node_attributes(G, community_map, 'community')
```

---

## Step 8: Basic Visualization

```python
# Create basic network visualization
plt.figure(figsize=(12, 8))

# Use spring layout
pos = nx.spring_layout(G, k=1, iterations=50)

# Draw nodes colored by community
colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
for i, community in enumerate(communities):
    nx.draw_networkx_nodes(G, pos, nodelist=list(community),
                          node_color=[colors[i]], node_size=500, alpha=0.8)

# Draw edges with thickness based on weight
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, width=[w/2 for w in weights], alpha=0.6)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

plt.title("Conclave Character Network", size=16)
plt.axis('off')
plt.tight_layout()
plt.show()
```

---

## Step 9: Interactive Visualization with Plotly

<!-- _class: small-code -->

```python
# Create interactive network visualization
def create_interactive_network(G, centrality_df):
    pos = nx.spring_layout(G, k=1, iterations=50)

    # Prepare node data
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = [f"{node}<br>Degree: {degree_centrality[node]:.3f}<br>Betweenness: {betweenness_centrality[node]:.3f}"
                 for node in G.nodes()]
    node_size = [degree_centrality[node] * 50 + 10 for node in G.nodes()]
    node_color = [community_map[node] for node in G.nodes()]

    # Prepare edge data
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create plot
    fig = go.Figure()

    # Add edges
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                            line=dict(width=1, color='gray'),
                            hoverinfo='none', showlegend=False))

    # Add nodes
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                            marker=dict(size=node_size, color=node_color,
                                      colorscale='Set3', line=dict(width=1)),
                            text=[node.split()[-1] for node in G.nodes()],
                            textposition="middle center",
                            hovertext=node_text, hoverinfo='text',
                            showlegend=False))

    fig.update_layout(title="Interactive Conclave Character Network",
                     showlegend=False, hovermode='closest',
                     margin=dict(b=20,l=5,r=5,t=40),
                     xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                     yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

    return fig

# Create and display interactive plot
interactive_fig = create_interactive_network(G, centrality_df)
interactive_fig.show()
```

---

## Step 10: AI-Enhanced Relationship Analysis

**Set up Claude API for relationship type inference:**

```python
import anthropic

# Set up Claude client (you'll need an API key)
client = anthropic.Anthropic(
    api_key="your_anthropic_api_key_here"  # Replace with your key
)

def infer_relationship_types(interactions_sample):
    """Use Claude to infer relationship types from context."""

    # Prepare sample interactions for analysis
    sample_text = "\n\n".join([
        f"Characters: {char1} and {char2}\nContext: {context[:200]}..."
        for char1, char2, context in interactions_sample[:10]
    ])

    prompt = f"""
    Analyze the following character interactions from the movie "Conclave" and classify the relationship types.

    For each pair of characters, determine their relationship type from these categories:
    - Allies/Friends
    - Rivals/Opponents
    - Superior/Subordinate
    - Neutral/Professional
    - Romantic/Personal

    Interactions:
    {sample_text}

    Provide your analysis in this format:
    Character1 - Character2: Relationship Type (brief explanation)
    """

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content

# Analyze relationships (if you have Claude API access)
# relationship_analysis = infer_relationship_types(interactions)
# print("AI-Inferred Relationships:")
# print(relationship_analysis)
```

---

## Step 11: Advanced Network Metrics

```python
# Calculate additional network metrics
def analyze_network_structure(G):
    metrics = {}

    # Basic metrics
    metrics['nodes'] = G.number_of_nodes()
    metrics['edges'] = G.number_of_edges()
    metrics['density'] = nx.density(G)

    # Connectivity
    metrics['is_connected'] = nx.is_connected(G)
    if nx.is_connected(G):
        metrics['diameter'] = nx.diameter(G)
        metrics['avg_path_length'] = nx.average_shortest_path_length(G)

    # Clustering
    metrics['avg_clustering'] = nx.average_clustering(G)
    metrics['transitivity'] = nx.transitivity(G)

    # Small-world properties
    # Compare with random graph
    random_G = nx.erdos_renyi_graph(G.number_of_nodes(), nx.density(G))
    metrics['clustering_ratio'] = metrics['avg_clustering'] / nx.average_clustering(random_G)

    return metrics

# Analyze network structure
network_metrics = analyze_network_structure(G)
print("Network Structure Analysis:")
for metric, value in network_metrics.items():
    print(f"{metric}: {value}")
```

---

## Step 12: Character Importance Ranking

```python
# Create comprehensive character ranking
def rank_characters(G, centrality_df):
    # Normalize centrality measures
    for col in ['Degree', 'Betweenness', 'Closeness', 'Eigenvector']:
        centrality_df[f'{col}_norm'] = (centrality_df[col] - centrality_df[col].min()) / (centrality_df[col].max() - centrality_df[col].min())

    # Calculate composite importance score
    centrality_df['Importance_Score'] = (
        centrality_df['Degree_norm'] * 0.3 +
        centrality_df['Betweenness_norm'] * 0.3 +
        centrality_df['Closeness_norm'] * 0.2 +
        centrality_df['Eigenvector_norm'] * 0.2
    )

    # Add network properties
    centrality_df['Connections'] = [G.degree(node) for node in centrality_df['Character']]
    centrality_df['Community'] = [community_map[node] for node in centrality_df['Character']]

    return centrality_df.sort_values('Importance_Score', ascending=False)

# Rank characters
character_ranking = rank_characters(G, centrality_df.copy())
print("Character Importance Ranking:")
print(character_ranking[['Character', 'Importance_Score', 'Connections', 'Community']].head(10))
```

---

## Step 13: Visualization Dashboard

```python
# Create a comprehensive visualization dashboard
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Network plot
ax1 = axes[0, 0]
pos = nx.spring_layout(G, k=1, iterations=50)
node_sizes = [degree_centrality[node] * 1000 + 100 for node in G.nodes()]
node_colors = [community_map[node] for node in G.nodes()]

nx.draw(G, pos, ax=ax1, node_size=node_sizes, node_color=node_colors,
        cmap=plt.cm.Set3, with_labels=True, font_size=8, font_weight='bold')
ax1.set_title("Character Network")

# 2. Centrality comparison
ax2 = axes[0, 1]
top_chars = character_ranking.head(8)
x_pos = range(len(top_chars))
ax2.bar(x_pos, top_chars['Degree'], alpha=0.7, label='Degree')
ax2.bar(x_pos, top_chars['Betweenness'], alpha=0.7, label='Betweenness')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([name.split()[-1] for name in top_chars['Character']], rotation=45)
ax2.set_title("Centrality Measures")
ax2.legend()

# 3. Degree distribution
ax3 = axes[1, 0]
degrees = [G.degree(node) for node in G.nodes()]
ax3.hist(degrees, bins=10, alpha=0.7, edgecolor='black')
ax3.set_title("Degree Distribution")
ax3.set_xlabel("Degree")
ax3.set_ylabel("Frequency")

# 4. Community sizes
ax4 = axes[1, 1]
community_sizes = [len(community) for community in communities]
ax4.pie(community_sizes, labels=[f"Community {i+1}" for i in range(len(communities))],
        autopct='%1.1f%%')
ax4.set_title("Community Sizes")

plt.tight_layout()
plt.show()
```

---

## Step 14: Export Results

```python
# Save results for further analysis
def export_results(G, character_ranking, network_metrics):
    # Save network as GraphML
    nx.write_graphml(G, "conclave_network.graphml")

    # Save character rankings
    character_ranking.to_csv("character_rankings.csv", index=False)

    # Save network metrics
    with open("network_metrics.txt", "w") as f:
        for metric, value in network_metrics.items():
            f.write(f"{metric}: {value}\n")

    # Save edge list with weights
    edge_data = []
    for u, v, data in G.edges(data=True):
        edge_data.append([u, v, data['weight']])

    edge_df = pd.DataFrame(edge_data, columns=['Source', 'Target', 'Weight'])
    edge_df.to_csv("network_edges.csv", index=False)

    print("Results exported:")
    print("- conclave_network.graphml (network file)")
    print("- character_rankings.csv (character analysis)")
    print("- network_metrics.txt (network properties)")
    print("- network_edges.csv (edge list)")

# Export all results
export_results(G, character_ranking, network_metrics)

# Download files in Colab
from google.colab import files
files.download("character_rankings.csv")
files.download("network_metrics.txt")
```

---

## Key Insights from the Analysis

**What we discovered about "Conclave" character network:**

1. **Central Characters:** Identify the most influential characters in the story
2. **Community Structure:** Reveal factions and alliances within the Vatican
3. **Network Properties:** Understand the social dynamics of the papal election
4. **Relationship Patterns:** Discover hidden connections and power structures

**Network Analysis Applications:**
- **Literary Analysis:** Character development and story structure
- **Social Dynamics:** Understanding group behavior and influence
- **Narrative Structure:** Identifying key plot points and character arcs

---

## Extensions and Improvements

**Try these enhancements on your own:**

1. **Temporal Analysis:** Track relationship changes throughout the screenplay
2. **Sentiment Analysis:** Analyze the emotional tone of interactions
3. **Scene-based Networks:** Create separate networks for different scenes
4. **Dialogue Analysis:** Weight relationships by amount of dialogue
5. **Character Attributes:** Add node attributes (age, position, nationality)
6. **Comparative Analysis:** Compare with other political thriller networks

**Advanced Techniques:**
- Multi-layer networks (formal vs. informal relationships)
- Dynamic network analysis (relationship evolution)
- Predictive modeling (outcome prediction based on network structure)

---

## Key Takeaways

- **Text Processing:** NER and proximity-based relationship extraction
- **Network Construction:** From raw text to structured graph data
- **Centrality Analysis:** Identifying important characters quantitatively
- **Community Detection:** Revealing hidden group structures
- **Visualization:** Multiple approaches for network presentation
- **AI Integration:** Enhancing analysis with language models
