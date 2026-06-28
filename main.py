try:
    from parsing import ParseMap
    from pydantic import ValidationError
    from models import Map
    from graph import Graph
    from find_line_number_line import LineError
    from paths_finder import PathFinder
    from Simulation_Engin import Simulation
    from colors import ANSI_COLORS
    from typing import Any
    from sys import argv
    from drones import Drone

    def main(map: list[Any]) -> None:

        if len(argv) <= 1:
            raise ValueError(
                "Execution Error: Missing map file argument.\n"
                "Reason: You must provide the path to a map "
                "file as a command-line argument.\n"
                "Usage: python3 main.py <path_to_map_file>"
            )

        ob: Any = ParseMap(argv[1])
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
                "Reason: Both 'start_hub' and 'end_hub' are strictly required."
                "Please define them in your map file."
            )

        ob = Map(**map[0])
        graph: Any = Graph(ob.zones, ob.connections)
        start: list[str] = [str(s.name) for s in ob.zones
                            if s.key.value == 'start_hub']

        end: list[str] = [str(e.name) for e in ob.zones
                          if e.key.value == 'end_hub']

        graph = graph.build_graph()

        zone_types: dict[str, str] = {z.name: (z.type.value
                                               if hasattr(z.type, 'value')
                                               else z.type) for z in ob.zones}

        find_paths_ob: PathFinder = PathFinder(zone_types, graph, ob.nb_drones,
                                               start[0], end[0],
                                               ob.zones, ob.connections)

        best_pathes: list[list[str]] = find_paths_ob.chose_path()

        if (len(best_pathes) == 0):
            raise ValueError(
                "Simulation Error: No valid path found.\n"
                "Reason: The end_hub is completely "
                "unreachable from the start_hub."
                "Please check the connections in the map file."
            )

        path_true_costs: list[int] = []

        for p in best_pathes:
            cost: int = 0

            for zone_name in p[1:]:
                z_type: str = zone_types[zone_name]

                cost += 2 if z_type == 'restricted' else 1

            path_true_costs.append(cost)

        drones: list[Drone] = []

        path_loads: list[int] = [0] * len(best_pathes)

        for i in range(ob.nb_drones):
            best_idx: int = 0

            best_expected_time: float = float('inf')

            for p_idx in range(len(best_pathes)):
                expected_time: float = float(
                    path_true_costs[p_idx] + path_loads[p_idx])

                if expected_time < best_expected_time:
                    best_expected_time = expected_time

                    best_idx = p_idx

            chosen_path: list[str] = best_pathes[best_idx]

            drones.append(Drone(i, f"D{i+1}", chosen_path))

            path_loads[best_idx] += 1

        simulation: Simulation = Simulation(zone_types, drones, ob.zones,
                                            ob.connections,
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

        except FileNotFoundError:
            print("File Error: The specified map file was not found.")

            print(f"Reason: No such file or directory: '{argv[1]}'.")

            print("Please check the path and try again.")

        except PermissionError:
            print("Permission Error: Access denied.")

            print("Reason: You do not have the required ", end='')

            print(f"permissions to read the file '{argv[1]}'.")

            print("Please check the file permissions ", end='')

            print("(e.g., using 'ls -l') and try again.")


except KeyboardInterrupt:
    print("\nExit.....")
    exit(1)
