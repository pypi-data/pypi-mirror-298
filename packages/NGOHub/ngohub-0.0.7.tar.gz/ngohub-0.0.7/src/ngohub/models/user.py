from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    created_on: datetime
    updated_on: datetime
    cognito_id: str
    name: str
    email: str
    phone: str
    role: str
    status: str
    organization_id: int
