*This project has been created as part of the 42 curriculum by ymajji.*

# 🚁 Fly-in: Autonomous Drone Routing System

## 📖 Description

Fly-in is a simulation project focused on routing a fleet of autonomous drones through a network of interconnected zones.

The objective is to move all drones from a starting hub to a destination hub in the minimum possible number of simulation turns while respecting a set of constraints imposed by the map.

The system must handle:

* Multiple drones moving simultaneously
* Zone capacity limitations
* Connection capacity limitations
* Restricted zones
* Priority zones
* Collision avoidance
* Traffic congestion

The project is implemented using an object-oriented architecture and models the problem as a weighted graph.

---

## ⚙️ Instructions

### Requirements

* Python 3.10+
* pip

### Install Dependencies

```bash
make install
```

This command installs the required packages:

* pydantic
* mypy
* flake8

### Run the Simulation

```bash
make run
```

or

```bash
python3 main.py
```

### Run Linting

```bash
make lint
```

For stricter type checking:

```bash
make lint-strict
```

### Debug Mode

```bash
make debug
```

### Clean Generated Files

```bash
make clean
```

---

## 🧠 Algorithm Choices & Implementation Strategy

### Data Validation

The project uses Pydantic models to validate all parsed map data before execution.

This guarantees:

* Early error detection
* Clear validation messages
* Consistent internal data structures

### Graph Construction

The map is represented as a weighted graph:

* Nodes represent zones
* Edges represent connections

Each zone contributes a traversal cost according to its type.

### Pathfinding

The routing engine is based on Dijkstra's algorithm implemented using Python's heapq module.

Traversal costs are adjusted according to zone types:

| Zone Type  | Cost            |
| ---------- | --------------- |
| Priority   | 1             |
| Normal     | 1           |
| Restricted | 2           |
| Blocked    | Not Traversable |

### Load Balancing Strategy

Using a single shortest path for every drone quickly creates congestion.

To mitigate this issue:

1. The shortest path is computed.
2. Its nodes receive a large penalty.
3. Dijkstra is executed again.
4. Alternative paths are generated.
5. Multiple path combinations are evaluated.

This strategy encourages traffic distribution across the graph.

### Bottleneck Analysis

Before the simulation starts, candidate paths are evaluated based on:

* Zone capacities
* Link capacities
* Estimated traffic flow

The path combination expected to minimize the total number of turns is selected.

### Simulation Engine

The simulation progresses turn by turn.

For every movement, the engine verifies:

* Zone occupancy
* Link occupancy
* Capacity constraints
* Travel duration

This prevents illegal movements and capacity violations.

---

## 🎨 Visual Representation

The simulator provides colorized terminal output.

When a zone specifies a color through the map metadata:

```text
[color=gold]
```

the destination zone is displayed using the corresponding ANSI terminal color.

This visual feedback improves the user experience by making it easier to:

* Follow drone movements
* Identify congested areas
* Distinguish different zones
* Understand traffic distribution

The visualization is lightweight and works directly in the terminal without requiring any external graphical interface.

---

## 📚 Resources

The following resources were particularly useful during the development of this project:

### Graph Theory

* Graph Theory Overview
  https://en.wikipedia.org/wiki/Graph_theory

### Dijkstra's Algorithm

* Dijkstra's Algorithm Explained (Computerphile)
  https://www.youtube.com/watch?v=GazC3A4OQTE

* Dijkstra's Algorithm (Wikipedia)
  https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm


### Multi-Agent Routing Concepts

* Multi-Agent Path Finding (MAPF)
  https://mapf.info/

### Simulation Concepts

* Discrete-Event Simulation
  https://en.wikipedia.org/wiki/Discrete-event_simulation

### AI Usage

AI was used for:

* Understanding graph theory concepts.
* Learning Dijkstra's algorithm and pathfinding techniques.
* Exploring simulation engine design.
* Brainstorming load-balancing and routing strategies.
* Investigating difficult bugs and implementation challenges.

All architectural decisions, implementation details, debugging, testing, and final code were completed by the author.
