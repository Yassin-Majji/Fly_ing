from drones import Drone
from typing import Any


class Simulation:
    def __init__(
            self, type_zones, drones: list[Drone], zones: list[Any],
            connections: list[Any],
            paths: list[list[str]],
            graph: dict[str, list[tuple[float, str]]],
            end: str
            ) -> None:

        self.type_zones = type_zones
        self.zones: list[Any] = zones

        self.connections: list[Any] = connections

        self.paths: list[list[str]] = paths

        self.number_drones_in_zone: dict[str, int] = {z: 0 for p in paths
                                                      for z in p}

        self.max_drones_for_this_zone: dict[str, float] = {z.name: z.max_drones
                                                           for z in zones}
        self.max_drones_for_this_zone[end] = float('inf')

        self.links_usage: dict[str, int] = {}

        self.drones: list[Drone] = drones

        self.results: list[list[str]] = []

        self.max_drones_for_this_link: dict[str, int] = {}

        self.on_the_goal: list[bool] = [False] * len(drones)

        self.graph: dict[str, list[tuple[float, str]]] = graph

        self.end: str = end

    def get_link_capacity(self, zone_target: str, zone_from: str) -> int:
        link_capacity: int = [c.max_link_capacity for c in self.connections
                              if ((c.zon1 == zone_target
                                   or c.zon2 == zone_target)
                                  and (c.zon1 == zone_from
                                       or c.zon2 == zone_from))][0]
        return link_capacity

    def determine_max_drones_in_link(self) -> None:
        z: str
        for z in self.graph:
            links: list[tuple[float, str]] = self.graph[z]
            zone: tuple[float, str]
            for zone in links:
                self.max_drones_for_this_link[f"{z}-{zone[1]}"] = (
                    self.get_link_capacity(z, zone[1]))

    def sort_drones_for_turn(self) -> list[Drone]:
        def sorting_key(drone: Drone) -> tuple[int, int]:
            priority_1: int = 0 if drone.in_link else 1
            priority_2: int = -drone.current_index
            return (priority_1, priority_2)

        sorted_drones: list[Drone] = sorted(self.drones, key=sorting_key)
        return sorted_drones

    def drones_tracker(self) -> list[list[str]]:
        self.determine_max_drones_in_link()

        while True:
            turns: list[str] = []

            nmbr_drones_on_road: dict[str, int] = {}

            c: Any
            for c in self.connections:
                nmbr_drones_on_road[f'{c.zon1}-{c.zon2}'] = 0
                nmbr_drones_on_road[f'{c.zon2}-{c.zon1}'] = 0

            drones: list[Drone] = self.sort_drones_for_turn()

            for d in drones:
                if all(self.on_the_goal):
                    return self.results

                if d.is_on_the_goal():
                    self.on_the_goal[d.id] = True
                    continue

                current_zone: str = d.get_current_zone()

                next_zone: str = d.get_next_zone()

                if d.in_link:
                    d.move()

                    d.in_link = False

                    turns.append(f"{d.name}-{next_zone}")

                    continue

                if (
                    self.number_drones_in_zone[next_zone]
                    == self.max_drones_for_this_zone[next_zone]
                    or nmbr_drones_on_road[f"{next_zone}-{current_zone}"]
                    == min(
                        self.max_drones_for_this_link
                        [f"{next_zone}-{current_zone}"],
                        self.max_drones_for_this_zone[next_zone]
                           )
                ):
                    continue

                next_zone_type: Any = self.type_zones[next_zone]

                if next_zone_type in ('normal', 'priority'):
                    d.move()

                    nmbr_drones_on_road[f"{next_zone}-{current_zone}"] += 1

                    self.number_drones_in_zone[next_zone] += 1

                    self.number_drones_in_zone[current_zone] -= 1

                    turns.append(f"{d.name}-{next_zone}")

                else:
                    d.in_link = True

                    nmbr_drones_on_road[f"{next_zone}-{current_zone}"] += 1

                    self.number_drones_in_zone[next_zone] += 1

                    self.number_drones_in_zone[current_zone] -= 1

                    turns.append(f"{d.name}-{current_zone}-{next_zone}")

            self.results.append(turns)

    def put_turns(self, turns: list[list[str]],
                  colors: dict[str, str]) -> None:

        t: list[str]

        for t in turns:
            d: str

            for d in t:
                parts: list[str] = d.split('-')

                if len(parts) > 2:
                    print(d, end=' ')

                else:
                    color: str = [z.color for z in self.zones
                                  if z.name == parts[-1]][0]

                    color_code: str | None = colors.get(color, None)

                    reset_code: str | None = colors.get('reset')

                    if not color_code:
                        print(d, end=' ')

                    else:
                        parts = d.rsplit('-', 1)

                        print(f"{parts[0]}-", end='')

                        print(f"{color_code}{parts[-1]}{reset_code}", end=' ')
            print()
