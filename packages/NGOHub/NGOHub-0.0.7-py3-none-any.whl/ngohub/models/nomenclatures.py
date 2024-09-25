from dataclasses import dataclass
from datetime import datetime


@dataclass
class Domain:
    id: int
    name: str
    created_on: datetime
    updated_on: datetime
