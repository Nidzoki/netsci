---
marp: true
theme: default
paginate: true
footer: 'Network Analysis - PMF-UNIST 2025/2026'
---

# Introduction to Network Science

Network Analysis - Lecture 1
Nikola Balic, Faculty of Natural Science, University of Split
Data Science and Engineering Master Program

---

## Why This Course Exists

- Many systems are better understood as relationships, not isolated objects.
- If we only list the objects, we miss the structure.
- If we study the connections, we can ask better questions.

---

## A Foundational Example

![width:1200px](images/konigsberg_bridges.png)

---

## Why Konigsberg Matters

- Euler treated a city-walking puzzle as a problem of connections.
- The exact map mattered less than which land areas were linked.
- That shift helped launch graph-based thinking.
- The big lesson: structure alone can answer important questions.

---

## What Is a Network?

A network is a set of **nodes** connected by **edges**.

- **Nodes** are entities: people, proteins, airports, web pages.
- **Edges** are relationships: friendship, regulation, flights, hyperlinks.
- The same representation works across many domains.

---

## Common Network Types

- **Undirected:** a connection has no direction
- **Directed:** a connection goes from one node to another
- **Weighted:** a connection has strength or frequency
- **Bipartite:** two different node types connect

These types matter because they change the analysis.

---

## Why Network Thinking Matters

Network analysis helps answer questions such as:

- Which nodes are most central or influential?
- How quickly can information, disease, or failure spread?
- Does the network break if a key node is removed?
- Are there communities or hidden subgroups?
- Is the structure random, clustered, or hub-dominated?

This course is about learning how to answer these questions rigorously.

---

## Example Domains

- **Social networks:** friendship, trust, influence, collaboration
- **Biological networks:** gene regulation, protein interactions, metabolism
- **Technological networks:** internet routing, power grids, road systems
- **Information networks:** web links, citation networks, recommendation systems
- **Economic networks:** trade, ownership, supply chains, financial contagion

Different domains use different data, but many structural questions are the same.

---

## What Structure Can Reveal

Even a small network can reveal:

- who is well connected,
- who links otherwise separate groups,
- which parts are isolated,
- and where the whole structure looks fragile.

Lecture 02 will formalize the graph concepts behind these observations.

---

## Why Networks Are Different From Tables

- A table describes attributes of items.
- A network describes relationships between items.
- Often the relationships are the main source of insight.

Tables tell us what something is.
Networks help us understand how things interact.

---

## What This Course Builds Toward

The course follows a cumulative path:

1. Graph foundations
2. Network measures and centrality
3. Connectivity and vulnerability
4. Community detection
5. Random, small-world, and scale-free models
6. Resilience and cascading failures
7. Dynamics on networks
8. Applied case studies

Each step adds a new way to study the same topic.

---

## How You Will Work In This Course

- You will not switch topics every week.
- Each student keeps one topic for the full course.
- Exercise 02 starts the topic.
- Later exercises extend the same analysis with new methods.

The course is designed as cumulative work, not isolated weekly tasks.

---

## Software and Tools

We will primarily use:

- **Python** for implementation
- **NetworkX** for graph construction and analysis
- **Jupyter notebooks** for iterative exploration
- **Gephi** or plotting libraries for visualization when useful

The goal is not tool memorization.
The goal is clear structural reasoning supported by code.

---

## Assessment

- Assignments: 30%
- Project: 40%
- Final exam: 30%

Assignments build skill.
The project develops your topic into a full analysis.

---

## Resources

- Main textbook: *Networks: An Introduction* by M. E. J. Newman
- Additional reference: *Network Science* by Albert-Laszlo Barabasi
- Additional reference: *Social and Economic Networks* by Matthew O. Jackson
- Additional reference: *The Atlas for the Aspiring Network Scientist* by Michele Coscia ([arXiv](https://arxiv.org/abs/2101.00863))
- Course materials: [NTDS 2019 - Network Data Science (EPFL)](https://github.com/mdeff/ntds_2019)
- Practical documentation: NetworkX official documentation

Use the books for concepts and the documentation for implementation.

---

## What You Should Be Able To Do By The End

By the end of the course, you should be able to:

- represent real data as a graph,
- compute and interpret network metrics,
- identify important nodes and communities,
- compare real networks with simple models,
- analyze resilience and diffusion processes,
- and communicate findings clearly with code, figures, and interpretation.

---

## Next Lecture

Next: **Graph Theory Fundamentals**

In [`lectures/02/lecture.md`](../02/lecture.md) we move from motivation to structure:

- graph construction,
- graph types,
- graph representations,
- and basic graph properties in NetworkX.

---

## Discussion: Apply The Questions

In discussion, apply the three questions to these examples:

1. A university class
2. International air travel
3. Scientific publishing in one field

Ask:

- What are the entities?
- What are the connections?
- What might become visible once we focus on structure?

---

## Three Questions To Keep In Mind

When you look at a system, ask:

1. What are the entities?
2. What are the connections between them?
3. What becomes visible once I focus on the structure?
