from typing import Any


class Graph:
    def __init__(self, zones: list[Any], connections: list[Any]) -> None:
        self.graph: dict[str, list[tuple[float, str]]] = {}
        self.zones: list[Any] = zones
        self.connections: list[Any] = connections

    def cost(self, type_zon: Any) -> float:
        if type_zon != 'normal':
            type_zon = type_zon.value
        if type_zon == 'priority':
            return 0.9
        elif type_zon == 'normal':
            return 1.0
        elif type_zon == 'restricted':
            return 2.0
        else:
            return 99999.0

    def zone_type(self, zone_name: str) -> Any:
        z: Any
        for z in self.zones:
            if z.name == zone_name:
                return (z.type)

    def build_graph(self) -> dict[str, list[tuple[float, str]]]:
        z: Any
        for z in self.zones:
            self.graph[z.name] = []
            c: Any
            for c in self.connections:
                if c.zon1 == z.name:
                    self.graph[z.name].append((self.cost(
                        self.zone_type(c.zon2)), c.zon2))
                elif c.zon2 == z.name:
                    self.graph[z.name].append((
                        self.cost(self.zone_type(c.zon1)), c.zon1))
        return self.graph
