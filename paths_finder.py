from dijkstra import ShortPath
from drones import Drone
from Simulation_Engin import Simulation
from typing import Any, Optional


class PathFinder:
    def __init__(self, zone_types: dict[str, str],
                 graph: dict[str, list[tuple[float, str]]],
                 nb_drones: int,
                 start: str,
                 end: str,
                 zones: list[Any],
                 connections: list[Any]) -> None:

        self.zone_types: dict[str, str] = zone_types

        self.best_paths: list[tuple[list[str], int, int]] = []

        self.graph: dict[str, list[tuple[float, str]]] = graph

        self.best_turns: float = float('inf')

        self.nb_drones: int = nb_drones

        self.connections: list[Any] = connections

        self.zones: list[Any] = zones

        self.start: str = start

        self.end: str = end

    def increase_path_cost(self, path: list[str]) -> None:

        for i in range(len(path) - 1):
            current_zone: str = path[i]

            next_zone: str = path[i + 1]

            current_zone_link: list[tuple[float, str]] = (
                self.graph[current_zone])

            for j, zone in enumerate(current_zone_link):
                if zone[1] == next_zone:
                    self.graph[current_zone][j] = (zone[0] + 2.0, next_zone)

            next_zone_link: list[tuple[float, str]] = self.graph[next_zone]

            for j, zone in enumerate(next_zone_link):
                if zone[1] == current_zone:
                    self.graph[next_zone][j] = (zone[0] + 2.0, current_zone)

    def chose_path(self) -> list[list[str]]:
        paths_finding: list[list[str]] = []

        find_the_same_path: int = 0

        while True:
            ob: ShortPath = ShortPath(self.zone_types, self.graph, self.start,
                                      self.end)

            shortest_path: Optional[list[str]] = ob.short_path()

            if not shortest_path:
                break

            if shortest_path in paths_finding:
                if find_the_same_path == 5:
                    break

                find_the_same_path += 1

                self.increase_path_cost(shortest_path)

                continue
            paths_finding.append(shortest_path)

            path_true_costs: list[int] = []

            for p in paths_finding:
                p_cost: int = 0

                for zone_name in p[1:]:
                    z_type: str = self.zone_types[zone_name]

                    p_cost += 2 if z_type == 'restricted' else 1

                path_true_costs.append(p_cost)

            test_drones: list[Drone] = []

            path_loads: list[int] = [0] * len(paths_finding)

            for i in range(self.nb_drones):
                best_idx: int = 0

                best_expected_time: float = float('inf')

                for p_idx in range(len(paths_finding)):
                    expected_time: float = float(path_true_costs[p_idx]
                                                 + path_loads[p_idx])

                    if expected_time < best_expected_time:
                        best_expected_time = expected_time

                        best_idx = p_idx

                path_to_assign: list[str] = paths_finding[best_idx]

                test_drones.append(Drone(i, f"D{i+1}", path_to_assign))

                path_loads[best_idx] += 1

            sim_engine: Simulation = Simulation(self.zone_types,
                                                test_drones,
                                                self.zones,
                                                self.connections,
                                                paths_finding, self.graph,
                                                self.end)

            real_turns_result: int = len(sim_engine.drones_tracker())
            if real_turns_result < self.best_turns:
                self.best_turns = float(real_turns_result)

                self.increase_path_cost(shortest_path)

            else:
                paths_finding.pop()

                break

        return paths_finding
