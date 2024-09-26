# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Tool", "Function"]


class Function(BaseModel):
    description: Optional[str] = None

    name: Optional[object] = None

    parameters: Optional[object] = None


class Tool(BaseModel):
    function: Function
    """Function definition"""

    name: str

    api_call: Optional[object] = None

    inherited: Optional[bool] = None

    integration: Optional[object] = None

    system: Optional[object] = None

    type: Optional[Literal["function", "integration", "system", "api_call"]] = None
