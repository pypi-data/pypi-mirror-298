# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ToolPatchParams", "Function"]


class ToolPatchParams(TypedDict, total=False):
    agent_id: Required[str]

    api_call: Optional[object]

    function: Optional[Function]
    """Function definition"""

    integration: Optional[object]

    name: Optional[str]

    system: Optional[object]

    type: Literal["function", "integration", "system", "api_call"]


class Function(TypedDict, total=False):
    description: Optional[str]

    name: Optional[object]

    parameters: Optional[object]
