from dataclasses import dataclass
from typing import Union

from ngohub.models.organization import OrganizationApplication
from ngohub.models.user import User


@dataclass
class CheckOrganizationUserApplication:
    user: Union[User, None]
    application: Union[OrganizationApplication, None]
    has_access: Union[bool, None]

    def __init__(self) -> None:
        self.user = None
        self.application = None
        self.has_access = None
