# Network Analysis

Course materials for Network Science (Network Analysis) taught by Nikola Balic at the Faculty of Natural Science, University of Split (PMF-UNIST) for the Data Science and Engineering Master program (2024/2025).

## Course Overview

This repository contains materials for the Network Analysis course, focusing on the principles, methods, and applications of network science for data science students.

## Assignments

The course includes assignment designed to evaluate students' understanding of network analysis concepts and techniques. This assignment involves working with real-world data to solve practical problems using the tools and methods taught in the course.

This assignment focuses on the fundamentals of network analysis, including:
- Network construction and representation
- Calculation and interpretation of network metrics
- Analysis of network structure and properties
- Identification of important nodes and communities

Resources: [assignment][a1q], [solution][a1s]

[a1q]: https://nbviewer.jupyter.org/github/nkkko/ns_2025/blob/outputs/assignments/1_network_science.ipynb
[a1s]: https://nbviewer.jupyter.org/github/nkkko/ns_2025/blob/outputs/assignments/1_network_science_solution.ipynb

## Semester Project

The final component of the course is an open-ended semester project that allows students to apply network analysis techniques to real-world problems. This project serves as a comprehensive assessment of both theoretical understanding and practical implementation skills.

### Project Overview
- Students propose and carry out network analysis projects on datasets of their choosing
- Projects should demonstrate mastery of concepts from both Network Science and Learning with Graphs
- We provide a [list of datasets and project ideas](projects) to help students get started
- Students engage in peer review to provide feedback and internalize the [grading criteria](projects/grading.md)

### Project Goals
Students can choose to focus their project in one of two directions:
1. **Tell a Network Data Story**: Analyze a network dataset to uncover and communicate insights about patterns, structures, and phenomena
2. **Build a Network-Based Application**: Develop a practical application or tool that leverages network analysis techniques

### Project Process
1. **Proposal**: Students submit a project proposal outlining their research question or application
2. **Development**: Implementation of network analysis and/or machine learning techniques
3. **Peer Review**: Students review each other's work to provide constructive feedback
4. **Final Submission**: Complete project with code, documentation, and findings
5. **Presentation**: Short presentation of key findings and methods

All student code will be stored in GitHub repositories and can be accessed via `git clone --recurse-submodules https://github.com/nkkko/ns_2025`, with one folder per student in `projects/code`.

## Grading Structure

The course grade is determined by three main components:

### 1. Assignments (40%)
* **Purpose**: Assess understanding of core network analysis concepts and techniques
* **Format**: Two structured assignments covering Network Science and Learning with Graphs
* **Evaluation**: Based on correctness, methodology, and clarity of explanation

### 2. Peer Review (20%)
* **Purpose**: Develop critical evaluation skills and deeper understanding of network analysis approaches
* **Format**: Each student evaluates peers' projects using the [5 grading criteria](projects/grading.md)
* **Evaluation**: Based on the thoroughness, constructiveness, and insight of feedback

### 3. Semester Project (40%)
* **Purpose**: Demonstrate comprehensive understanding and application of network analysis
* **Format**: Open-ended project analyzing real-world network data
* **Evaluation**: Based on technical implementation, analytical depth, and communication of insights

This structure ensures a balanced assessment of both theoretical knowledge and practical application skills in network analysis.

## Repository Structure

- `lectures/`: Marp slide decks and supporting image-generation scripts
- `tutorials/`: Jupyter notebooks for practical tutorials
- `exercises/`: Assignment and exercise prompts
- `projects/`: Semester project guidance and grading materials
- `sources/`: Reference notes and imported source material

## Prerequisites

- Python 3.12+
- Jupyter Notebook/Lab
- NetworkX, Pandas, NumPy, Matplotlib, and other required libraries

## Setting Up

### Option 1: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver.

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Clone the repository
git clone https://github.com/nibzard/netsci.git

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/nibzard/netsci.git

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Nikola Balic
