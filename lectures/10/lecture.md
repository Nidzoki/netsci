---
marp: true
theme: default
paginate: true
footer: 'Network Analysis - PMF-UNIST 2025/2026'

<style>
section pre code {
  font-size: 0.8em; /* Slightly smaller code font for more content */
  line-height: 1.2;
}
img[alt~="right"] {
  float: right;
  margin-left: 20px;
  margin-bottom: 10px;
}
img[alt~="left"] {
  float: left;
  margin-right: 20px;
  margin-bottom: 10px;
}
</style>
---

# Dynamics on Networks
## How Behaviors, Information, and Failures Spread

Network Analysis - Lecture 10
Nikola Balic, Faculty of Natural Science, University of Split
Data Science and Engineering Master Program

---

## Recap & Today's Focus

- **Previous Lectures:** Network fundamentals, measures, models (ER, WS, BA), connectivity, communities, and resilience.
- **L09 (Resilience):** Focused on network robustness and vulnerability to failures.
- **Today:** We shift from static structure to **processes unfolding *on* networks over time.**
    - How does the network structure influence the spread of diseases, information, opinions, or failures?
    - What are the fundamental models describing these dynamic processes?

---

## 1. What is Network Dynamics?

**Network Dynamics** is the study of processes that occur on networks, where the state of nodes or edges changes over time due to interactions.

- **Interplay:**
    - Network structure (topology) influences how dynamics unfold.
    - Dynamical processes can, in turn, alter the network structure (adaptive networks).
- **Importance:** Understanding network dynamics helps us predict, control, and design for:
    - Spread of diseases, information, or innovations.
    - Formation of collective opinions or behaviors.
    - Stability and collapse of complex systems.

---

## 2. Core Concepts in Network Dynamics

- **States & Transitions:** Nodes (or edges) can be in different states (e.g., susceptible/infected, active/inactive, opinion A/B). Transitions occur based on rules and neighbor states.
- **Time:**
    - **Discrete-time:** Processes evolve in steps.
    - **Continuous-time:** Processes evolve continuously.
- **Thresholds:** Critical points where a small change can lead to a large shift in system behavior (e.g., epidemic outbreak, information cascade).
- **Feedback Loops:** The outcome of a dynamic process can influence future steps of the same or other processes.

---

## 3. Diffusion & Information Spreading

How do things (information, innovations, behaviors) spread through a network?

- **Simple Contagion:**
    - Exposure to **one** active neighbor is enough to activate a node.
    - Examples: Some infectious diseases, basic information.
- **Complex Contagion:**
    - Requires exposure to **multiple** active neighbors or social reinforcement.
    - Examples: Adoption of costly innovations, risky behaviors, social norms.

---

### Independent Cascade (IC) Model

A model for simple contagion:
1. Starts with an initial set of active ("infected") nodes.
2. In each discrete time step:
   - Newly activated nodes get **one chance** to activate their inactive neighbors.
   - Activation attempt succeeds with a probability *p*.
3. If successful, the neighbor becomes active in the next time step.
4. The process continues until no more activations are possible.

![width:700px alt="right"](images/independent_cascade_steps.png)
*Conceptual visualization of IC: Node A activates B (prob p1). Then B attempts to activate C (prob p2) and D (prob p3). Node D fails to activate.*

---

### Linear Threshold (LT) Model

A model often used for complex contagion:
1. Each node *i* has a **threshold** $\theta_i$ (e.g., randomly chosen between 0 and 1).
2. Each edge (*j*,*i*) from an active neighbor *j* to *i* has a weight $w_{ji}$ such that $\sum_j w_{ji} \le 1$.
3. A node *i* becomes active if the sum of weights from its already active neighbors meets or exceeds its threshold:
   $\sum_{\text{active neighbors }j} w_{ji} \ge \theta_i$.
4. Process continues until no more nodes can be activated.

---

![width:600px alt="right"](images/linear_threshold_steps.png)
*Conceptual visualization of LT: Node X has a threshold $\theta_X$. In Step 1, active neighbors A & B provide influence, but it's below $\theta_X$. In Step 2, C also becomes active, and the combined influence from A, B, & C meets or exceeds $\theta_X$, so X activates.*

---

### Factors Influencing Information Spread

- **Network Topology:**
    - **Hubs (High-degree nodes):** Can be super-spreaders in simple contagion.
    - **Bridges (Nodes connecting communities):** Crucial for spreading between groups.
    - **Community Structure:** Dense communities can trap information or facilitate rapid local spread.
- **Content Characteristics:**
    - Virality, novelty, emotional appeal.
- **Individual Behavior:**
    - Susceptibility, adoption thresholds.

---

## 4. Epidemic Models on Networks

Modeling the spread of infectious diseases.

- **Compartmental Models:** Nodes transition between states:
    - **S:** Susceptible (can get infected)
    - **E:** Exposed (infected but not yet infectious - optional)
    - **I:** Infected (can spread the disease)
    - **R:** Recovered (immune or removed)

---

### SIS (Susceptible-Infected-Susceptible) Model

- Nodes transition: S $\xrightarrow{\beta}$ I $\xrightarrow{\gamma}$ S
    - $\beta$: Infection rate (probability of S getting I from an I neighbor).
    - $\gamma$: Recovery rate (probability of I becoming S).
- No permanent immunity.
- Can lead to an **endemic state** where the disease persists.

---

![width:700px alt="right"](images/sis_model.png)
*Left: SIS state transitions. Right: Prevalence curve showing initial rise of Infected (I/N) and settling to an endemic level, with Susceptible (S/N) mirroring this.*

---

### SIR (Susceptible-Infected-Recovered) Model

- Nodes transition: S $\xrightarrow{\beta}$ I $\xrightarrow{\gamma}$ R
    - $\beta$: Infection rate.
    - $\gamma$: Recovery rate (leading to immunity).
- Individuals gain permanent immunity after recovery.
- Results in an **epidemic curve** (rise and fall of infections).
- Concept of **herd immunity**.

---

![width:700px alt="right"](images/sir_model.png)
*Left: SIR state transitions. Right: Prevalence curves for S, I, R over time, showing the characteristic rise and fall of the Infected (I/N) population.*

---

### SEIR (Susceptible-Exposed-Infected-Recovered) Model

- Nodes transition: S $\xrightarrow{\beta}$ E $\xrightarrow{\sigma}$ I $\xrightarrow{\gamma}$ R
    - Adds an **Exposed (E)** state: infected but not yet infectious.
    - $\sigma$: Rate of moving from Exposed to Infected (1/latency period).
- More realistic for diseases with an incubation period.

---

### Basic Reproduction Number ($R_0$)

- **Definition:** The average number of secondary infections caused by a single infected individual in a fully susceptible population.
- **$R_0$ on Networks:**
    - Influenced by network structure, particularly the degree distribution.
    - For a specific infected node *i*: $R_0^{(i)} = \sum_{j \in \text{neighbors}} (\text{prob. of transmission to } j)$
    - Average $R_0 = \langle R_0^{(i)} \rangle$ over all nodes.
    - In heterogeneous networks (like scale-free): $R_0 \approx \frac{\beta}{\gamma} \left( \frac{\langle k^2 \rangle}{\langle k \rangle} \right)$. Hubs disproportionately drive spread.
- **Epidemic Threshold:**
    - If $R_0 > 1$, an epidemic can spread.
    - If $R_0 < 1$, the infection dies out.
    - Vaccination aims to reduce effective $R_0$ below 1.

---

## 5. Opinion Dynamics

Modeling how opinions form, diffuse, and evolve in social networks.

- **Voter Model:**
    - Each node holds one of a few discrete opinions.
    - In each step, a random node adopts the opinion of a randomly chosen neighbor.
    - Leads to consensus in finite connected networks, but can be slow. Coarsening occurs where regions of same opinion grow.

---

![width:700px alt="right"](images/voter_model_evolution.png)
*Visualization of Voter Model: From initial random opinions, domains of like-opinions form and expand, eventually leading to network-wide consensus (or polarization in variants).*

---

### DeGroot Model (Opinion Averaging)

- Opinions are continuous values (e.g., between 0 and 1).
- Each node updates its opinion to the weighted average of its neighbors' opinions (including its own, often with self-weight $W_{ii}$).
  $x_i(t+1) = \sum_j W_{ij} x_j(t)$, where $W$ is a row-stochastic matrix (rows sum to 1).
- Consensus is reached if the network (viewed as a Markov chain with transition matrix $W$) is strongly connected and aperiodic. The consensus value depends on the network structure and initial opinions.

---

### Bounded Confidence Models

E.g., Deffuant-Weisbuch model:
1. Opinions are continuous values $x_i \in [0,1]$.
2. Each node *i* only interacts with neighbors *j* if their opinion difference $|x_i - x_j|$ is less than a confidence bound $\epsilon$.
3. If they interact, they adjust their opinions towards each other:
   $x_i(t+1) = x_i(t) + \mu(x_j(t) - x_i(t))$
   $x_j(t+1) = x_j(t) + \mu(x_i(t) - x_j(t))$ (where $\mu$ is a convergence parameter, e.g., 0.5)
- Can lead to **opinion polarization** (multiple distinct opinion clusters) or **fragmentation** if $\epsilon$ is small.

---

![width:600px alt="right"](images/bounded_confidence_model.png)
*Visualization: An initial random distribution of opinions (left) evolves into distinct opinion clusters (right) due to the bounded confidence rule. Nodes only interact if their opinions are "close enough."*

---

### Echo Chambers & Filter Bubbles

- **Echo Chambers:** People primarily interact with and hear opinions similar to their own, reinforcing existing beliefs.
- **Filter Bubbles:** Personalized content algorithms (e.g., on social media) limit exposure to diverse perspectives, creating an environment where one's own views are overrepresented.
- Network structure (homophily, community structure) and opinion dynamics (like bounded confidence) interact to create and sustain these phenomena, potentially leading to increased polarization.

---

## 6. Cascading Failures (Dynamics Perspective)

Recap from L09: Cascades involve initial failures triggering subsequent ones. Here, we focus on the *dynamical models*.

- **Threshold Models (revisited for failures):**
    - A node fails if a certain fraction (or number) of its neighbors have failed, or if its operational load exceeds its capacity.
    - Load on a node can be its degree, betweenness, or a functional load. Capacity is a predefined limit.
    - If a node fails, its load is redistributed to its operational neighbors. If a neighbor's new total load > capacity, it also fails.
    - Example: Watts' model for global cascades on random networks.

---

- **Sandpile Models (Self-Organized Criticality):**
    - Nodes accumulate "stress" (like grains of sand).
    - When stress on a node exceeds a threshold, it "topples," distributing units of stress to its neighbors.
    - This can trigger neighbors to topple, leading to "avalanches" of various sizes (often showing a power-law distribution of avalanche sizes).
    - Illustrates how systems can naturally evolve to a critical state where small perturbations can have large consequences.

---

![width:650px alt="right"](images/sandpile_model.png)
*Conceptual illustration: A grid where cells accumulate 'sand'. One cell topples (center panel), distributing sand to neighbors, some of which then topple (right panel), creating an avalanche.*

---

### Modeling Overload and Interdependence

- **Overload Models:** Focus on network flow (e.g., electricity, data packets), node capacities, and specific load redistribution rules. When a node fails, its traffic/load must be rerouted, potentially overloading other components.
- **Interdependent Networks (revisited):**
    - Failure in Network A (e.g., power grid) causes dependent nodes in Network B (e.g., communication network controlling power stations) to fail.
    - This, in turn, can cause further failures in Network A, leading to a feedback loop of escalating failures.
    - Dynamics involve coupled failure propagations between networks.

---

## 7. Synchronization (Brief Overview)

- **Definition:** A process where interacting elements (oscillators) in a network adjust their individual rhythms or behaviors to achieve a common, collective pattern (e.g., same phase or frequency).
- **Examples:**
    - Fireflies flashing in unison.
    - Neurons firing synchronously in the brain.
    - Applause in an audience becoming synchronized.
    - Coupled pendulums adjusting their swing.

---

- **Kuramoto Model:** A standard mathematical model for synchronization of coupled oscillators. Each oscillator *i* has a natural frequency $\omega_i$ and its phase $\theta_i$ evolves according to:
    $ \dot{\theta}_i = \omega_i + \frac{K}{N} \sum_{j=1}^{N} A_{ij} \sin(\theta_j - \theta_i) $
    where $K$ is the coupling strength, $N$ is the number of oscillators, and $A_{ij}=1$ if $i,j$ are connected.
- **Factors:** Network topology (shorter paths, higher clustering can aid synchronization) and coupling strength ($K$) determine if and how fast synchronization occurs.

---

## 8. NetworkX for Simulating Dynamics (Conceptual)

While NetworkX is excellent for structural analysis, simulating complex dynamics often requires custom code or specialized libraries built on top of it (like EoN for epidemics).

**General Approach for a Simple SIR Simulation in NetworkX:**
1.  **Initialization:**
    - Create your graph `G` in NetworkX.
    - Assign initial states (e.g., 'S', 'I', 'R') as node attributes.
    ```python
    nx.set_node_attributes(G, 'S', 'status')
    # Example: Infect one node
    initial_infected_node = list(G.nodes())
    G.nodes[initial_infected_node]['status'] = 'I'
    ```

---

2.  **Iteration (Time Steps):**
    - Loop for a number of time steps or until no 'I' nodes remain.
    - In each step, identify nodes that will change state (e.g., S to I, I to R) based on model rules (e.g., probabilities $\beta, \gamma$ and neighbor states).
    - Store these intended changes.
    - *After* checking all nodes for potential transitions in the current step, apply the stored changes to update node attributes. This avoids using a state that just changed within the same time step.
    - Record counts of S, I, R nodes for plotting.

---

## 9. Applications (Expanded)

- **Public Health:**
    - **Epidemic Models (SIR, SEIR):** Predicting outbreaks, evaluating vaccination strategies (e.g., targeting hubs vs. random immunization), assessing impact of NPIs (non-pharmaceutical interventions like lockdowns, social distancing).
- **Information/Social Media:**
    - **Diffusion Models (IC, LT):** Understanding viral marketing, rumor spread, adoption of innovations, misinformation campaigns. Identifying key influencers or "patient zero" of a trend.
    - **Opinion Dynamics:** Analyzing political polarization, the formation of social norms, and the impact of echo chambers and filter bubbles on societal discourse.

---

- **Infrastructure & Finance:**
    - **Cascading Failure Models:** Assessing robustness of power grids, communication networks, transportation systems, and financial markets (systemic risk). Identifying critical interdependencies and vulnerabilities.
- **Ecology:**
    - Modeling the spread of invasive species, dynamics of predator-prey relationships in food webs, disease propagation in animal or plant populations, and resilience of ecosystems.
- **Neuroscience:**
    - Understanding synchronization of neural activity, spread of signals in the brain, and how network structure relates to cognitive functions or neurological disorders.

---

## 10. Key Takeaways & Future Directions

- Network structure is not just a static backdrop; it actively shapes and is shaped by dynamic processes occurring upon it.
- Different models (diffusion, epidemic, opinion, cascade, synchronization) capture distinct mechanisms of spread, change, and collective behavior.
- Thresholds, feedback loops, and the role of specific network features (hubs, bridges, communities) are critical to understanding the outcomes of these dynamics.
- Simulating network dynamics allows us to test hypotheses, predict real-world phenomena, and design effective interventions or more resilient systems.

---

**Future Directions:**
- Dynamics on **temporal networks** (where connections change over time).
- Dynamics on **multilayer networks** (where nodes participate in multiple types of networks simultaneously).
- **Adaptive networks** where the network structure and the dynamic process co-evolve (e.g., unfriending someone with opposing views).
- Leveraging **AI/ML** for predicting, controlling, and optimizing dynamics on complex networks.
