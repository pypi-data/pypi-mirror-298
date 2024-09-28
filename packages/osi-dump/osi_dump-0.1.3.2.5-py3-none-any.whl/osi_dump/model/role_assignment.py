from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


class RoleAssignment(BaseModel):
    model_config = ConfigDict(strict=True)

    user_id: Optional[str]

    user_name: Optional[str]
    
    user_enabled: Optional[bool]

    role_id: Optional[str]

    role_name: Optional[str]

    scope: Optional[dict]
