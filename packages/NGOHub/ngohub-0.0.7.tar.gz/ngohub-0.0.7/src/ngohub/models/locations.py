from dataclasses import dataclass
from datetime import datetime


@dataclass
class City:
    id: int
    name: str
    county_id: int
    created_on: datetime


@dataclass
class County:
    id: int
    name: str
    abbreviation: str
    region_id: int
    created_on: datetime
