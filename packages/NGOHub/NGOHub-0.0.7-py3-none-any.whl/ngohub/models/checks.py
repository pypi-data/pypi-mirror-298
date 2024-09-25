from dataclasses import dataclass
from typing import Dict, Union

from ngohub.models.organization import OrganizationApplication


@dataclass
class CheckOrganizationUserApplication:
    user: Union[Dict, None]
    application: Union[OrganizationApplication, None]
    has_access: Union[bool, None]

    def __init__(self) -> None:
        self.user = None
        self.application = None
        self.has_access = None
