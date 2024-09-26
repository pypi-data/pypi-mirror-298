# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ToolCreateParams", "Function"]


class ToolCreateParams(TypedDict, total=False):
    function: Required[Function]
    """Function definition"""

    name: Required[str]

    api_call: Optional[object]

    integration: Optional[object]

    system: Optional[object]

    type: Literal["function", "integration", "system", "api_call"]


class Function(TypedDict, total=False):
    description: Optional[str]

    name: Optional[object]

    parameters: Optional[object]
