from pydantic import BaseModel, Field
from enum import Enum


class ZonesKey(Enum):
    start_hub = 'start_hub'
    hub = 'hub'
    end_hub = 'end_hub'


class ZonesType(Enum):
    NORMAL = 'normal'
    PRIORITY = 'priority'
    RESTRICTED = 'restricted'
    BLOCKED = 'blocked'


class Connection(BaseModel):
    line_number: int
    line: str
    zon1: str
    zon2: str
    max_link_capacity: int = Field(default=1, ge=1)


class Zone(BaseModel):
    key: ZonesKey
    name: str
    x: int
    y: int
    color: str | None = Field(default=None)
    max_drones: int = Field(ge=1, default=1)
    type: ZonesType = Field(default=ZonesType.NORMAL)


class Map(BaseModel):
    line_number: int
    line: str
    nb_drones: int = Field(gt=0)
    zones: list[Zone]
    connections: list[Connection]
