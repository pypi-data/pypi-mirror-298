# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ToolListResponse", "Function"]


class Function(BaseModel):
    description: Optional[str] = None

    name: Optional[object] = None

    parameters: Optional[object] = None


class ToolListResponse(BaseModel):
    id: str

    created_at: datetime

    function: Function
    """Function definition"""

    name: str

    updated_at: datetime

    api_call: Optional[object] = None

    integration: Optional[object] = None

    system: Optional[object] = None

    type: Optional[Literal["function", "integration", "system", "api_call"]] = None
