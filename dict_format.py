from typing import TypedDict


class ZoneDict(TypedDict, total=False):
    key: str
    name: str
    x: str
    y: str
    color: str
    zone: str
    line: str
    line_number: int


class ConnectionDict(TypedDict):
    zon1: str
    zon2: str
    line: str
    line_number: int


class ParsedMap(TypedDict):
    key: str
    zones: list[ZoneDict]
    connections: list[ConnectionDict]
    nb_drones: str
    line: str
    line_number: int
