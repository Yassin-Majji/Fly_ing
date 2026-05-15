from pydantic import BaseModel, Field, model_validator
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


class Zone(BaseModel):
    key: ZonesKey
    name: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    color: str = Field(default=None)
    max_drones: int = Field(ge=1, default=1)
    type: ZonesType = Field(default='normal')
    error_zone: dict[str, str] = {}

    @model_validator(mode='before')
    @classmethod
    def handle(cls, zone):
        cls.error_zone = {'line': zone['line'], 'line_number': zone['line_number']}
        return zone


class Connection(BaseModel):
    zon1: str
    zon2: str
    max_link_capacity: int = Field(default=1, ge=1)
    error_conn: dict[str, str] = {}

    @model_validator(mode='before')
    @classmethod
    def handle(cls, conn):
        cls.error_conn = {'line': conn['line'], 'line_number': conn['line_number']}
        return conn


class Map(BaseModel):
    nb_drones: int = Field(gt=0)
    zones: list[Zone]
    connections: list[Connection]
    error_nb: dict[str, str] = {}

    @model_validator(mode='before')
    @classmethod
    def handle(cls, map):
        cls.error_nb = {'line': map['line'], 'line_number': map['line_number']}
        return map
