from drones import Drone
from typing import Any


class Simulation:
    def __init__(
            self, zones: list[Any],
            connections: list[Any],
            nb_drones: int,
            paths: list[tuple[list[str], int, int]],
            graph: dict[str, list[tuple[float, str]]],
            end: str
            ) -> None:

        self.zones: list[Any] = zones
        self.connections: list[Any] = connections
        self.nb_drones: int = nb_drones
        self.paths: list[tuple[list[str], int, int]] = paths
        self.number_drones_in_zone: dict[str, int] = {z: 0 for p in paths
                                                      for z in p[0]}
        self.max_drones_for_this_zone: dict[str, float] = {z.name: z.max_drones
                                                           for z in zones}
        self.max_drones_for_this_zone[end] = float('inf')
        self.links_usage: dict[str, int] = {}
        self.drones: list[Drone] = []
        self.results: list[list[str]] = []
        self.max_drones_for_this_link: dict[str, int] = {}
        self.on_the_goal: list[bool] = [False] * nb_drones
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

    def drones_setup(self) -> None:
        number_drones_in_paths: list[int] = [0] * len(self.paths)
        j: int
        for j in range(self.nb_drones):
            drone_costs: list[tuple[int, int]] = []
            i: int
            p: tuple[list[str], int, int]
            for i, p in enumerate(self.paths):
                drone_costs += [(p[1] + number_drones_in_paths[i] // p[2], i)]
            chosen_path: tuple[int, int] = min(drone_costs, key=lambda t: t[0])
            number_drones_in_paths[chosen_path[1]] += 1
            self.drones += [Drone('D' + str(j + 1),
                                  self.paths[chosen_path[1]][0])]

    def drones_tracker(self) -> list[list[str]]:
        self.drones_setup()
        self.determine_max_drones_in_link()
        while True:
            turns: list[str] = []
            nmbr_drones_on_road: dict[str, int] = {}
            c: Any
            for c in self.connections:
                nmbr_drones_on_road[f'{c.zon1}-{c.zon2}'] = 0
                nmbr_drones_on_road[f'{c.zon2}-{c.zon1}'] = 0
            number_drones_to_goal: dict[str, int] = {z[1]: 0
                                                     for z in self.graph
                                                     [self.end]}

            i: int
            d: Drone
            for i, d in enumerate(self.drones):

                if all(self.on_the_goal):
                    return self.results

                if d.is_on_the_goal():
                    continue

                current_zone: str = d.get_current_zone()

                next_zone: str = d.get_next_zone()

                if d.on_the_link():
                    d.in_link = False

                    d.move()

                    turns += [f"{d.name}-{next_zone}"]

                    if next_zone == self.end:
                        self.on_the_goal[i] = True

                    continue

                next_zone_type: Any = [z.type for z in self.zones
                                       if z.name == next_zone][0]

                if next_zone_type != 'normal':
                    next_zone_type = next_zone_type.value

                if next_zone_type == 'normal' or next_zone_type == 'priority':
                    if next_zone == self.end:
                        if (
                            number_drones_to_goal[current_zone] <
                            self.max_drones_for_this_link
                            [f"{next_zone}-{current_zone}"]
                        ):
                            d.move()
                            self.on_the_goal[i] = True
                            number_drones_to_goal[current_zone] += 1
                            self.number_drones_in_zone[current_zone] -= 1
                            turns += [f"{d.name}-{next_zone}"]
                        continue

                    if (
                        nmbr_drones_on_road[f"{next_zone}-{current_zone}"] <
                        min(
                            self.max_drones_for_this_zone[next_zone],
                            self.max_drones_for_this_link
                            [f"{next_zone}-{current_zone}"]
                            )
                    ):
                        d.move()
                        self.number_drones_in_zone[current_zone] -= 1
                        self.number_drones_in_zone[next_zone] += 1
                        turns += [f"{d.name}-{next_zone}"]
                        nmbr_drones_on_road[f"{next_zone}-{current_zone}"] += 1

                else:
                    if (
                        nmbr_drones_on_road[f"{next_zone}-{current_zone}"] <
                        min(
                            self.max_drones_for_this_zone[next_zone],
                            self.max_drones_for_this_link
                            [f"{next_zone}-{current_zone}"]
                            )
                    ):
                        if next_zone == self.end:
                            if (
                                number_drones_to_goal[current_zone] <
                                self.max_drones_for_this_link
                                [f"{next_zone}-{current_zone}"]
                            ):
                                self.number_drones_in_zone[current_zone] -= 1

                        d.in_link = True
                        turns += [f"{d.name}-{current_zone}-{next_zone}"]
                        self.number_drones_in_zone[current_zone] -= 1
                        self.number_drones_in_zone[current_zone] += 1
                        nmbr_drones_on_road[f"{next_zone}-{current_zone}"] += 1

            self.results.append(turns)

    def put_turns(self, turns: list[list[str]],
                  colors: dict[str, str]) -> None:
        print(f"\n\n   number turns is   {len(turns)}")
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
                    color_code: str | None = colors.get(color.lower(), None)
                    reset_code: str | None = colors.get('reset')
                    if not color_code:
                        print(d, end=' ')
                    else:
                        parts = d.rsplit('-', 1)
                        print(f"{parts[0]}-", end='')
                        print(f"{color_code}{parts[-1]}{reset_code}", end=' ')
            print()
