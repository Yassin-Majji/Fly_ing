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
* pydantic
* mypy
* flake8

### Install Dependencies

```bash
make install
```

This command installs the required packages:

* pydantic
* mypy
* flake8

### Run the Simulation

To run the simulation, pass the map file to the run command:
```bash
make run FILE=maps/easy.txt
```
*(or manually: `python3 main.py maps/easy.txt`)*

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

Using a shortest path for every drone quickly creates congestion.

To mitigate this issue:

1. The shortest path is computed.
2. Its nodes receive a large penalty.
3. Dijkstra is executed again.
4. Alternative paths are generated.
5. Multiple path combinations are evaluated.

This strategy encourages traffic distribution across the graph.

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

## 📋 Example Input (Map File)

```text
nb_drones: 2

start_hub: start 0 0
end_hub: goal 0 2

hub: mid 0 1

connection: start-mid
connection: mid-goal
```

---

## 📤 Example Output (Simulation Turns)

```text
D1-mid
D1-goal D2-mid
D2-goal
```

---

## 📚 Resources

The following resources were particularly useful during the development of this project:

### Graph Theory

* Graph Theory Overview
  https://www.youtube.com/watch?v=7zZ-VhLOy6M

### Dijkstra's Algorithm

* Dijkstra's Algorithm Explained (Computerphile)
  https://www.youtube.com/watch?v=GazC3A4OQTE

* Dijkstra's Algorithm (Wikipedia)
  https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

### AI Usage

AI was used for:

* Understanding graph theory concepts.
* Learning Dijkstra's algorithm and pathfinding techniques.
* Exploring simulation engine design.
* Brainstorming load-balancing and routing strategies.
* Investigating difficult bugs and implementation challenges.