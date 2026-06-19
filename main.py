from parsing import ParseMap
from pydantic import ValidationError
from models import Map
from graph import Graph
from find_line_number_line import LineError
from paths_finder import PathFinder
from Simulation_Engin import Simulation
from colors import ANSI_COLORS
from typing import Any


def main(map: list[Any]) -> None:
    ob: Any = ParseMap("maps/challenger/01_the_impossible_dream.txt")
    ob.read_lines()
    map[0] = ob.map
    keys: list[str] = [D['key'] for D in map[0]['zones']]
    if not map[0]['nb_drones']:
        raise ValueError(
            "Parse Error: Missing 'nb_drones' declaration.\n"
            "Reason: The map file must define the number of drones  "
            "(e.g., 'nb_drones: 5') at the very beginning."
            )

    if 'start_hub' not in keys or 'end_hub' not in keys:
        raise ValueError(
            "Parse Error: Missing mandatory hubs.\n"
            "Reason: Both 'start_hub' and 'end_hub' are strictly required. "
            "Please define them in your map file."
            )
    ob = Map(**map[0])
    graph: Any = Graph(ob.zones, ob.connections)
    start: list[str] = [str(s.name) for s in ob.zones
                        if s.key.value == 'start_hub']

    end: list[str] = [str(e.name) for e in ob.zones
                      if e.key.value == 'end_hub']

    graph = graph.build_graph()
    find_paths_ob: PathFinder = PathFinder(graph, ob.nb_drones,
                                           start[0], end[0],
                                           ob.zones, ob.connections)

    best_pathes: list[tuple[list[str], int, int]] = find_paths_ob.chose_path()
    if (len(best_pathes) == 0):
        raise ValueError(
            "Simulation Error: No valid path found.\n"
            "Reason: The end_hub is completely "
            "unreachable from the start_hub."
            "Please check the connections in the map file."
            )
    print(f"pathsm ---> {best_pathes}")
    simulation: Simulation = Simulation(ob.zones, ob.connections, ob.nb_drones,
                                        best_pathes, graph, end[0])
    turns: list[list[str]] = simulation.drones_tracker()
    simulation.put_turns(turns, ANSI_COLORS)


if __name__ == '__main__':
    try:
        map: list[Any] = [None]
        main(map)

    except ValidationError as e:
        first_error: Any = e.errors()[0]

        line: str
        line_number: int
        line, line_number = LineError.find_line_content_and_number_line(
            map[0],
            first_error['loc'])

        print(f"Data Validation Error at line {line_number}.")
        print(f"[{line_number}] {line}")
        print(f"Reason: {first_error['msg']}")

    except ValueError as e:
        print(e)
