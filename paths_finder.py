from dijkstra import ShortPath
from typing import Any


class PathFinder:
    def __init__(self, graph: dict[str, list[tuple[float, str]]],
                 nb_drones: int,
                 start: str,
                 end: str,
                 zones: list[Any],
                 connections: list[Any]) -> None:

        self.best_paths: list[tuple[list[str], int, int]] = []
        self.graph: dict[str, list[tuple[float, str]]] = graph
        self.best_turns: float = float('inf')
        self.nb_drones: int = nb_drones
        self.connections: list[Any] = connections
        self.zones: list[Any] = zones
        self.start: str = start
        self.end: str = end

    @staticmethod
    def find_bottle_neck(path: list[str], zones: list[Any],
                         connections: list[Any]) -> int:

        capacity: list[list[int]] = []
        i: int
        z: str
        for i, z in enumerate(path[1:], 1):
            capacity.append([zone.max_drones for zone in zones
                             if zone.name == z])
            capacity.append([c.max_link_capacity for c in connections
                             if (
                                 (c.zon1 == z or c.zon2 == z)
                                 and (
                                     c.zon1 == path[i - 1]
                                     or c.zon2 == path[i - 1])
                                 )])
        return min(capacity)[0]

    def increase_path_cost(self, path: list[str]) -> None:
        key: str
        zones: list[tuple[float, str]]
        for key, zones in self.graph.items():
            i: int
            for i in range(len(zones)):
                cost: float
                zone: str
                cost, zone = zones[i]
                if zone in path[1:len(path) - 1]:
                    self.graph[key][i] = (cost + 300.0, zone)

    @staticmethod
    def test_with_new_path(paths: list[tuple[list[str], int, int]],
                           nb_drones: int) -> int:

        number_drones_in_paths: list[int] = [0] * len(paths)
        turnes: int = 0
        _: int
        for _ in range(nb_drones):
            drone_costs: list[tuple[int, int]] = []
            i: int
            p: tuple[list[str], int, int]
            for i, p in enumerate(paths):
                drone_costs += [(p[1] + number_drones_in_paths[i] // p[2], i)]
            chosen_path: tuple[int, int] = min(drone_costs, key=lambda t: t[0])
            number_drones_in_paths[chosen_path[1]] += 1
            if chosen_path[0] > turnes:
                turnes = chosen_path[0]
        return turnes

    def chose_path(self) -> list[tuple[list[str], int, int]]:
        paths_finding: list[tuple[list[str], int, int]] = []
        while True:
            ob: ShortPath = ShortPath(self.graph, self.start, self.end)
            res: tuple[list[str], int] | None = ob.short_path()
            if not res:
                return self.best_paths
            shortest_path: list[str]
            cost: int
            shortest_path, cost = res
            paths_finding += [(shortest_path, cost,
                               PathFinder.find_bottle_neck(shortest_path,
                                                           self.zones,
                                                           self.connections))]
            turnes: int = PathFinder.test_with_new_path(
                paths_finding,
                self.nb_drones)

            if turnes >= self.best_turns:
                return self.best_paths
            self.increase_path_cost(shortest_path)
            self.best_turns = float(turnes)
            self.best_paths += [paths_finding[-1]]
