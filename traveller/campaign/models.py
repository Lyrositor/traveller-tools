from enum import Enum
from typing import Optional

from pydantic import BaseModel

from traveller.worldgen.models import TradeCode, Base, StarportQuality, TravelZone, RouteType


class MissionStatus(str, Enum):
    NEW = "new"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class MissionLog(BaseModel):
    date: str
    entry: str


class Mission(BaseModel):
    name: str
    intro: str
    status: MissionStatus = MissionStatus.NEW
    log: list[MissionLog] = []


class BorderDefinition(BaseModel):
    coordinates: list[str] = []
    allegiance: Optional[str] = None
    color: Optional[str] = None


class RouteDefinition(BaseModel):
    start: str
    start_offset_x: int = 0
    start_offset_y: int = 0
    end: str
    end_offset_x: int = 0
    end_offset_y: int = 0
    type: Optional[RouteType] = None


class HexDefinition(BaseModel):
    world_occurrence: Optional[bool] = None
    name: Optional[str] = None
    num_gas_giants: Optional[int] = None
    size: Optional[int] = None
    atmosphere: Optional[int] = None
    hydrographics: Optional[int] = None
    population: Optional[int] = None
    starport_quality: Optional[StarportQuality] = None
    government: Optional[int] = None
    law: Optional[int] = None
    tech: Optional[int] = None
    bases: Optional[list[Base]] = None
    allegiance: Optional[str] = None
    zone: Optional[TravelZone] = None
    trade_codes: Optional[list[TradeCode]] = None


class Campaign(BaseModel):
    name: str
    start_date: str
    current_date: str
    ship_name: str
    map_subsector: Optional[str] = None
    missions: list[Mission] = []
    sector_name: str
    sector_density_dm: int = 0
    subsectors: dict[str, str] = {}
    borders: list[BorderDefinition] = []
    routes: list[RouteDefinition] = []
    allegiances: dict[str, str] = {}
    map: dict[str, HexDefinition] = {}
