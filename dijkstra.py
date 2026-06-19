import heapq
from math import ceil


class ShortPath:
    def __init__(self, graph: dict[str, list[tuple[float, str]]],
                 start: str, end: str) -> None:
        self.graph: dict[str, list[tuple[float, str]]] = graph
        self.start: str = start
        self.end: str = end
        self.visited: set[str] = set()
        self.eq: list[tuple[float, str]] = [(0, start)]
        self.distances: dict[str, float] = {node: float('inf')
                                            for node in graph}
        self.distances[start] = 0
        self.previous: dict[str, str] = {}

    def short_path(self) -> tuple[list[str], int] | None:
        while self.eq:
            current_cost: float
            current_node: str
            current_cost, current_node = heapq.heappop(self.eq)

            if current_node == self.end:
                break
            if current_node in self.visited:
                continue

            self.visited.add(current_node)

            edge_cost: float
            neighbor: str
            for edge_cost, neighbor in self.graph[current_node]:
                if neighbor in self.visited:
                    continue

                new_cost: float = current_cost + edge_cost
                if new_cost < self.distances[neighbor]:
                    self.distances[neighbor] = new_cost
                    self.previous[neighbor] = current_node
                    heapq.heappush(self.eq, (new_cost, neighbor))

        if self.distances[self.end] == float('inf'):
            return None

        path: list[str] = []
        current: str = self.end

        while current in self.previous:
            path.append(current)
            current = self.previous[current]

        path.append(self.start)
        path.reverse()

        return path, ceil(self.distances[self.end])
