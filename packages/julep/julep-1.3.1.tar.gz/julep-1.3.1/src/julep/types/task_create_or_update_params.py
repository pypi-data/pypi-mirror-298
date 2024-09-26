# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .tool_param import ToolParam
from .chat_settings_param import ChatSettingsParam

__all__ = [
    "TaskCreateOrUpdateParams",
    "Main",
    "MainEvaluateStep",
    "MainToolCallStep",
    "MainPromptStepInput",
    "MainPromptStepInputPromptUnionMember0",
    "MainPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainGetStep",
    "MainSetStep",
    "MainLogStep",
    "MainEmbedStep",
    "MainEmbedStepEmbed",
    "MainSearchStep",
    "MainSearchStepSearch",
    "MainSearchStepSearchVectorDocSearchRequest",
    "MainSearchStepSearchTextOnlyDocSearchRequest",
    "MainSearchStepSearchHybridDocSearchRequest",
    "MainReturnStep",
    "MainSleepStep",
    "MainSleepStepSleep",
    "MainErrorWorkflowStep",
    "MainYieldStep",
    "MainWaitForInputStep",
    "MainWaitForInputStepWaitForInput",
    "MainIfElseWorkflowStepInput",
    "MainIfElseWorkflowStepInputThen",
    "MainIfElseWorkflowStepInputThenEvaluateStep",
    "MainIfElseWorkflowStepInputThenToolCallStep",
    "MainIfElseWorkflowStepInputThenPromptStepInput",
    "MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0",
    "MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainIfElseWorkflowStepInputThenGetStep",
    "MainIfElseWorkflowStepInputThenSetStep",
    "MainIfElseWorkflowStepInputThenLogStep",
    "MainIfElseWorkflowStepInputThenEmbedStep",
    "MainIfElseWorkflowStepInputThenEmbedStepEmbed",
    "MainIfElseWorkflowStepInputThenSearchStep",
    "MainIfElseWorkflowStepInputThenSearchStepSearch",
    "MainIfElseWorkflowStepInputThenSearchStepSearchVectorDocSearchRequest",
    "MainIfElseWorkflowStepInputThenSearchStepSearchTextOnlyDocSearchRequest",
    "MainIfElseWorkflowStepInputThenSearchStepSearchHybridDocSearchRequest",
    "MainIfElseWorkflowStepInputThenReturnStep",
    "MainIfElseWorkflowStepInputThenSleepStep",
    "MainIfElseWorkflowStepInputThenSleepStepSleep",
    "MainIfElseWorkflowStepInputThenErrorWorkflowStep",
    "MainIfElseWorkflowStepInputThenYieldStep",
    "MainIfElseWorkflowStepInputThenWaitForInputStep",
    "MainIfElseWorkflowStepInputThenWaitForInputStepWaitForInput",
    "MainIfElseWorkflowStepInputElse",
    "MainIfElseWorkflowStepInputElseEvaluateStep",
    "MainIfElseWorkflowStepInputElseToolCallStep",
    "MainIfElseWorkflowStepInputElsePromptStepInput",
    "MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0",
    "MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainIfElseWorkflowStepInputElseGetStep",
    "MainIfElseWorkflowStepInputElseSetStep",
    "MainIfElseWorkflowStepInputElseLogStep",
    "MainIfElseWorkflowStepInputElseEmbedStep",
    "MainIfElseWorkflowStepInputElseEmbedStepEmbed",
    "MainIfElseWorkflowStepInputElseSearchStep",
    "MainIfElseWorkflowStepInputElseSearchStepSearch",
    "MainIfElseWorkflowStepInputElseSearchStepSearchVectorDocSearchRequest",
    "MainIfElseWorkflowStepInputElseSearchStepSearchTextOnlyDocSearchRequest",
    "MainIfElseWorkflowStepInputElseSearchStepSearchHybridDocSearchRequest",
    "MainIfElseWorkflowStepInputElseReturnStep",
    "MainIfElseWorkflowStepInputElseSleepStep",
    "MainIfElseWorkflowStepInputElseSleepStepSleep",
    "MainIfElseWorkflowStepInputElseErrorWorkflowStep",
    "MainIfElseWorkflowStepInputElseYieldStep",
    "MainIfElseWorkflowStepInputElseWaitForInputStep",
    "MainIfElseWorkflowStepInputElseWaitForInputStepWaitForInput",
    "MainSwitchStepInput",
    "MainSwitchStepInputSwitch",
    "MainSwitchStepInputSwitchThen",
    "MainSwitchStepInputSwitchThenEvaluateStep",
    "MainSwitchStepInputSwitchThenToolCallStep",
    "MainSwitchStepInputSwitchThenPromptStepInput",
    "MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0",
    "MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainSwitchStepInputSwitchThenGetStep",
    "MainSwitchStepInputSwitchThenSetStep",
    "MainSwitchStepInputSwitchThenLogStep",
    "MainSwitchStepInputSwitchThenEmbedStep",
    "MainSwitchStepInputSwitchThenEmbedStepEmbed",
    "MainSwitchStepInputSwitchThenSearchStep",
    "MainSwitchStepInputSwitchThenSearchStepSearch",
    "MainSwitchStepInputSwitchThenSearchStepSearchVectorDocSearchRequest",
    "MainSwitchStepInputSwitchThenSearchStepSearchTextOnlyDocSearchRequest",
    "MainSwitchStepInputSwitchThenSearchStepSearchHybridDocSearchRequest",
    "MainSwitchStepInputSwitchThenReturnStep",
    "MainSwitchStepInputSwitchThenSleepStep",
    "MainSwitchStepInputSwitchThenSleepStepSleep",
    "MainSwitchStepInputSwitchThenErrorWorkflowStep",
    "MainSwitchStepInputSwitchThenYieldStep",
    "MainSwitchStepInputSwitchThenWaitForInputStep",
    "MainSwitchStepInputSwitchThenWaitForInputStepWaitForInput",
    "MainForeachStepInput",
    "MainForeachStepInputForeach",
    "MainForeachStepInputForeachDo",
    "MainForeachStepInputForeachDoEvaluateStep",
    "MainForeachStepInputForeachDoToolCallStep",
    "MainForeachStepInputForeachDoPromptStepInput",
    "MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0",
    "MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainForeachStepInputForeachDoGetStep",
    "MainForeachStepInputForeachDoSetStep",
    "MainForeachStepInputForeachDoLogStep",
    "MainForeachStepInputForeachDoEmbedStep",
    "MainForeachStepInputForeachDoEmbedStepEmbed",
    "MainForeachStepInputForeachDoSearchStep",
    "MainForeachStepInputForeachDoSearchStepSearch",
    "MainForeachStepInputForeachDoSearchStepSearchVectorDocSearchRequest",
    "MainForeachStepInputForeachDoSearchStepSearchTextOnlyDocSearchRequest",
    "MainForeachStepInputForeachDoSearchStepSearchHybridDocSearchRequest",
    "MainParallelStepInput",
    "MainParallelStepInputParallel",
    "MainParallelStepInputParallelEvaluateStep",
    "MainParallelStepInputParallelToolCallStep",
    "MainParallelStepInputParallelPromptStepInput",
    "MainParallelStepInputParallelPromptStepInputPromptUnionMember0",
    "MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainParallelStepInputParallelGetStep",
    "MainParallelStepInputParallelSetStep",
    "MainParallelStepInputParallelLogStep",
    "MainParallelStepInputParallelEmbedStep",
    "MainParallelStepInputParallelEmbedStepEmbed",
    "MainParallelStepInputParallelSearchStep",
    "MainParallelStepInputParallelSearchStepSearch",
    "MainParallelStepInputParallelSearchStepSearchVectorDocSearchRequest",
    "MainParallelStepInputParallelSearchStepSearchTextOnlyDocSearchRequest",
    "MainParallelStepInputParallelSearchStepSearchHybridDocSearchRequest",
    "MainMainInput",
    "MainMainInputMap",
    "MainMainInputMapEvaluateStep",
    "MainMainInputMapToolCallStep",
    "MainMainInputMapPromptStepInput",
    "MainMainInputMapPromptStepInputPromptUnionMember0",
    "MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1",
    "MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1Content",
    "MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel",
    "MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL",
    "MainMainInputMapGetStep",
    "MainMainInputMapSetStep",
    "MainMainInputMapLogStep",
    "MainMainInputMapEmbedStep",
    "MainMainInputMapEmbedStepEmbed",
    "MainMainInputMapSearchStep",
    "MainMainInputMapSearchStepSearch",
    "MainMainInputMapSearchStepSearchVectorDocSearchRequest",
    "MainMainInputMapSearchStepSearchTextOnlyDocSearchRequest",
    "MainMainInputMapSearchStepSearchHybridDocSearchRequest",
]


class TaskCreateOrUpdateParams(TypedDict, total=False):
    agent_id: Required[str]

    main: Required[Iterable[Main]]

    name: Required[str]

    description: str

    inherit_tools: bool

    input_schema: Optional[object]

    metadata: Optional[object]

    tools: Iterable[ToolParam]


class MainEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainPromptStepInputPromptUnionMember0ContentUnionMember1Content(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(TypedDict, total=False):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(TypedDict, total=False):
    image_url: Required[MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL]
    """The image URL"""

    type: Literal["image_url"]


MainPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainPromptStepInputPromptUnionMember0(_MainPromptStepInputPromptUnionMember0ReservedKeywords, total=False):
    content: Required[Union[List[str], Iterable[MainPromptStepInputPromptUnionMember0ContentUnionMember1], str]]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainGetStep(TypedDict, total=False):
    get: Required[str]


class MainSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainLogStep(TypedDict, total=False):
    log: Required[str]


class MainEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainEmbedStep(TypedDict, total=False):
    embed: Required[MainEmbedStepEmbed]


class MainSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainSearchStepSearch: TypeAlias = Union[
    MainSearchStepSearchVectorDocSearchRequest,
    MainSearchStepSearchTextOnlyDocSearchRequest,
    MainSearchStepSearchHybridDocSearchRequest,
]


class MainSearchStep(TypedDict, total=False):
    search: Required[MainSearchStepSearch]


_MainReturnStepReservedKeywords = TypedDict(
    "_MainReturnStepReservedKeywords",
    {
        "return": Dict[str, str],
    },
    total=False,
)


class MainReturnStep(_MainReturnStepReservedKeywords, total=False):
    pass


class MainSleepStepSleep(TypedDict, total=False):
    days: int

    hours: int

    minutes: int

    seconds: int


class MainSleepStep(TypedDict, total=False):
    sleep: Required[MainSleepStepSleep]


class MainErrorWorkflowStep(TypedDict, total=False):
    error: Required[str]


class MainYieldStep(TypedDict, total=False):
    workflow: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainWaitForInputStepWaitForInput(TypedDict, total=False):
    info: Required[Dict[str, str]]


class MainWaitForInputStep(TypedDict, total=False):
    wait_for_input: Required[MainWaitForInputStepWaitForInput]


class MainIfElseWorkflowStepInputThenEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputThenToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1Content(
    TypedDict, total=False
):
    text: Required[str]

    type: Literal["text"]


class MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(
    TypedDict, total=False
):
    image_url: Required[
        MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL
    ]
    """The image URL"""

    type: Literal["image_url"]


MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0(
    _MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[
            List[str],
            Iterable[MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0ContentUnionMember1],
            str,
        ]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainIfElseWorkflowStepInputThenPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainIfElseWorkflowStepInputThenPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainIfElseWorkflowStepInputThenGetStep(TypedDict, total=False):
    get: Required[str]


class MainIfElseWorkflowStepInputThenSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputThenLogStep(TypedDict, total=False):
    log: Required[str]


class MainIfElseWorkflowStepInputThenEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainIfElseWorkflowStepInputThenEmbedStep(TypedDict, total=False):
    embed: Required[MainIfElseWorkflowStepInputThenEmbedStepEmbed]


class MainIfElseWorkflowStepInputThenSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainIfElseWorkflowStepInputThenSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainIfElseWorkflowStepInputThenSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainIfElseWorkflowStepInputThenSearchStepSearch: TypeAlias = Union[
    MainIfElseWorkflowStepInputThenSearchStepSearchVectorDocSearchRequest,
    MainIfElseWorkflowStepInputThenSearchStepSearchTextOnlyDocSearchRequest,
    MainIfElseWorkflowStepInputThenSearchStepSearchHybridDocSearchRequest,
]


class MainIfElseWorkflowStepInputThenSearchStep(TypedDict, total=False):
    search: Required[MainIfElseWorkflowStepInputThenSearchStepSearch]


_MainIfElseWorkflowStepInputThenReturnStepReservedKeywords = TypedDict(
    "_MainIfElseWorkflowStepInputThenReturnStepReservedKeywords",
    {
        "return": Dict[str, str],
    },
    total=False,
)


class MainIfElseWorkflowStepInputThenReturnStep(
    _MainIfElseWorkflowStepInputThenReturnStepReservedKeywords, total=False
):
    pass


class MainIfElseWorkflowStepInputThenSleepStepSleep(TypedDict, total=False):
    days: int

    hours: int

    minutes: int

    seconds: int


class MainIfElseWorkflowStepInputThenSleepStep(TypedDict, total=False):
    sleep: Required[MainIfElseWorkflowStepInputThenSleepStepSleep]


class MainIfElseWorkflowStepInputThenErrorWorkflowStep(TypedDict, total=False):
    error: Required[str]


class MainIfElseWorkflowStepInputThenYieldStep(TypedDict, total=False):
    workflow: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainIfElseWorkflowStepInputThenWaitForInputStepWaitForInput(TypedDict, total=False):
    info: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputThenWaitForInputStep(TypedDict, total=False):
    wait_for_input: Required[MainIfElseWorkflowStepInputThenWaitForInputStepWaitForInput]


MainIfElseWorkflowStepInputThen: TypeAlias = Union[
    MainIfElseWorkflowStepInputThenEvaluateStep,
    MainIfElseWorkflowStepInputThenToolCallStep,
    MainIfElseWorkflowStepInputThenPromptStepInput,
    MainIfElseWorkflowStepInputThenGetStep,
    MainIfElseWorkflowStepInputThenSetStep,
    MainIfElseWorkflowStepInputThenLogStep,
    MainIfElseWorkflowStepInputThenEmbedStep,
    MainIfElseWorkflowStepInputThenSearchStep,
    MainIfElseWorkflowStepInputThenReturnStep,
    MainIfElseWorkflowStepInputThenSleepStep,
    MainIfElseWorkflowStepInputThenErrorWorkflowStep,
    MainIfElseWorkflowStepInputThenYieldStep,
    MainIfElseWorkflowStepInputThenWaitForInputStep,
]


class MainIfElseWorkflowStepInputElseEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputElseToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1Content(
    TypedDict, total=False
):
    text: Required[str]

    type: Literal["text"]


class MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(
    TypedDict, total=False
):
    image_url: Required[
        MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL
    ]
    """The image URL"""

    type: Literal["image_url"]


MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0(
    _MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[
            List[str],
            Iterable[MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0ContentUnionMember1],
            str,
        ]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainIfElseWorkflowStepInputElsePromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainIfElseWorkflowStepInputElsePromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainIfElseWorkflowStepInputElseGetStep(TypedDict, total=False):
    get: Required[str]


class MainIfElseWorkflowStepInputElseSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputElseLogStep(TypedDict, total=False):
    log: Required[str]


class MainIfElseWorkflowStepInputElseEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainIfElseWorkflowStepInputElseEmbedStep(TypedDict, total=False):
    embed: Required[MainIfElseWorkflowStepInputElseEmbedStepEmbed]


class MainIfElseWorkflowStepInputElseSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainIfElseWorkflowStepInputElseSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainIfElseWorkflowStepInputElseSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainIfElseWorkflowStepInputElseSearchStepSearch: TypeAlias = Union[
    MainIfElseWorkflowStepInputElseSearchStepSearchVectorDocSearchRequest,
    MainIfElseWorkflowStepInputElseSearchStepSearchTextOnlyDocSearchRequest,
    MainIfElseWorkflowStepInputElseSearchStepSearchHybridDocSearchRequest,
]


class MainIfElseWorkflowStepInputElseSearchStep(TypedDict, total=False):
    search: Required[MainIfElseWorkflowStepInputElseSearchStepSearch]


_MainIfElseWorkflowStepInputElseReturnStepReservedKeywords = TypedDict(
    "_MainIfElseWorkflowStepInputElseReturnStepReservedKeywords",
    {
        "return": Dict[str, str],
    },
    total=False,
)


class MainIfElseWorkflowStepInputElseReturnStep(
    _MainIfElseWorkflowStepInputElseReturnStepReservedKeywords, total=False
):
    pass


class MainIfElseWorkflowStepInputElseSleepStepSleep(TypedDict, total=False):
    days: int

    hours: int

    minutes: int

    seconds: int


class MainIfElseWorkflowStepInputElseSleepStep(TypedDict, total=False):
    sleep: Required[MainIfElseWorkflowStepInputElseSleepStepSleep]


class MainIfElseWorkflowStepInputElseErrorWorkflowStep(TypedDict, total=False):
    error: Required[str]


class MainIfElseWorkflowStepInputElseYieldStep(TypedDict, total=False):
    workflow: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainIfElseWorkflowStepInputElseWaitForInputStepWaitForInput(TypedDict, total=False):
    info: Required[Dict[str, str]]


class MainIfElseWorkflowStepInputElseWaitForInputStep(TypedDict, total=False):
    wait_for_input: Required[MainIfElseWorkflowStepInputElseWaitForInputStepWaitForInput]


MainIfElseWorkflowStepInputElse: TypeAlias = Union[
    MainIfElseWorkflowStepInputElseEvaluateStep,
    MainIfElseWorkflowStepInputElseToolCallStep,
    MainIfElseWorkflowStepInputElsePromptStepInput,
    MainIfElseWorkflowStepInputElseGetStep,
    MainIfElseWorkflowStepInputElseSetStep,
    MainIfElseWorkflowStepInputElseLogStep,
    MainIfElseWorkflowStepInputElseEmbedStep,
    MainIfElseWorkflowStepInputElseSearchStep,
    MainIfElseWorkflowStepInputElseReturnStep,
    MainIfElseWorkflowStepInputElseSleepStep,
    MainIfElseWorkflowStepInputElseErrorWorkflowStep,
    MainIfElseWorkflowStepInputElseYieldStep,
    MainIfElseWorkflowStepInputElseWaitForInputStep,
]

_MainIfElseWorkflowStepInputReservedKeywords = TypedDict(
    "_MainIfElseWorkflowStepInputReservedKeywords",
    {
        "if": str,
        "else": Optional[MainIfElseWorkflowStepInputElse],
    },
    total=False,
)


class MainIfElseWorkflowStepInput(_MainIfElseWorkflowStepInputReservedKeywords, total=False):
    then: Required[MainIfElseWorkflowStepInputThen]


class MainSwitchStepInputSwitchThenEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainSwitchStepInputSwitchThenToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1Content(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(
    TypedDict, total=False
):
    image_url: Required[
        MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL
    ]
    """The image URL"""

    type: Literal["image_url"]


MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0(
    _MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[
            List[str], Iterable[MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0ContentUnionMember1], str
        ]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainSwitchStepInputSwitchThenPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainSwitchStepInputSwitchThenPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainSwitchStepInputSwitchThenGetStep(TypedDict, total=False):
    get: Required[str]


class MainSwitchStepInputSwitchThenSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainSwitchStepInputSwitchThenLogStep(TypedDict, total=False):
    log: Required[str]


class MainSwitchStepInputSwitchThenEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainSwitchStepInputSwitchThenEmbedStep(TypedDict, total=False):
    embed: Required[MainSwitchStepInputSwitchThenEmbedStepEmbed]


class MainSwitchStepInputSwitchThenSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainSwitchStepInputSwitchThenSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainSwitchStepInputSwitchThenSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainSwitchStepInputSwitchThenSearchStepSearch: TypeAlias = Union[
    MainSwitchStepInputSwitchThenSearchStepSearchVectorDocSearchRequest,
    MainSwitchStepInputSwitchThenSearchStepSearchTextOnlyDocSearchRequest,
    MainSwitchStepInputSwitchThenSearchStepSearchHybridDocSearchRequest,
]


class MainSwitchStepInputSwitchThenSearchStep(TypedDict, total=False):
    search: Required[MainSwitchStepInputSwitchThenSearchStepSearch]


_MainSwitchStepInputSwitchThenReturnStepReservedKeywords = TypedDict(
    "_MainSwitchStepInputSwitchThenReturnStepReservedKeywords",
    {
        "return": Dict[str, str],
    },
    total=False,
)


class MainSwitchStepInputSwitchThenReturnStep(_MainSwitchStepInputSwitchThenReturnStepReservedKeywords, total=False):
    pass


class MainSwitchStepInputSwitchThenSleepStepSleep(TypedDict, total=False):
    days: int

    hours: int

    minutes: int

    seconds: int


class MainSwitchStepInputSwitchThenSleepStep(TypedDict, total=False):
    sleep: Required[MainSwitchStepInputSwitchThenSleepStepSleep]


class MainSwitchStepInputSwitchThenErrorWorkflowStep(TypedDict, total=False):
    error: Required[str]


class MainSwitchStepInputSwitchThenYieldStep(TypedDict, total=False):
    workflow: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainSwitchStepInputSwitchThenWaitForInputStepWaitForInput(TypedDict, total=False):
    info: Required[Dict[str, str]]


class MainSwitchStepInputSwitchThenWaitForInputStep(TypedDict, total=False):
    wait_for_input: Required[MainSwitchStepInputSwitchThenWaitForInputStepWaitForInput]


MainSwitchStepInputSwitchThen: TypeAlias = Union[
    MainSwitchStepInputSwitchThenEvaluateStep,
    MainSwitchStepInputSwitchThenToolCallStep,
    MainSwitchStepInputSwitchThenPromptStepInput,
    MainSwitchStepInputSwitchThenGetStep,
    MainSwitchStepInputSwitchThenSetStep,
    MainSwitchStepInputSwitchThenLogStep,
    MainSwitchStepInputSwitchThenEmbedStep,
    MainSwitchStepInputSwitchThenSearchStep,
    MainSwitchStepInputSwitchThenReturnStep,
    MainSwitchStepInputSwitchThenSleepStep,
    MainSwitchStepInputSwitchThenErrorWorkflowStep,
    MainSwitchStepInputSwitchThenYieldStep,
    MainSwitchStepInputSwitchThenWaitForInputStep,
]


class MainSwitchStepInputSwitch(TypedDict, total=False):
    case: Required[Union[Literal["_"], str]]

    then: Required[MainSwitchStepInputSwitchThen]


class MainSwitchStepInput(TypedDict, total=False):
    switch: Required[Iterable[MainSwitchStepInputSwitch]]


class MainForeachStepInputForeachDoEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainForeachStepInputForeachDoToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1Content(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(
    TypedDict, total=False
):
    image_url: Required[
        MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL
    ]
    """The image URL"""

    type: Literal["image_url"]


MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0(
    _MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[
            List[str], Iterable[MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0ContentUnionMember1], str
        ]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainForeachStepInputForeachDoPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainForeachStepInputForeachDoPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainForeachStepInputForeachDoGetStep(TypedDict, total=False):
    get: Required[str]


class MainForeachStepInputForeachDoSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainForeachStepInputForeachDoLogStep(TypedDict, total=False):
    log: Required[str]


class MainForeachStepInputForeachDoEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainForeachStepInputForeachDoEmbedStep(TypedDict, total=False):
    embed: Required[MainForeachStepInputForeachDoEmbedStepEmbed]


class MainForeachStepInputForeachDoSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainForeachStepInputForeachDoSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainForeachStepInputForeachDoSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainForeachStepInputForeachDoSearchStepSearch: TypeAlias = Union[
    MainForeachStepInputForeachDoSearchStepSearchVectorDocSearchRequest,
    MainForeachStepInputForeachDoSearchStepSearchTextOnlyDocSearchRequest,
    MainForeachStepInputForeachDoSearchStepSearchHybridDocSearchRequest,
]


class MainForeachStepInputForeachDoSearchStep(TypedDict, total=False):
    search: Required[MainForeachStepInputForeachDoSearchStepSearch]


MainForeachStepInputForeachDo: TypeAlias = Union[
    MainForeachStepInputForeachDoEvaluateStep,
    MainForeachStepInputForeachDoToolCallStep,
    MainForeachStepInputForeachDoPromptStepInput,
    MainForeachStepInputForeachDoGetStep,
    MainForeachStepInputForeachDoSetStep,
    MainForeachStepInputForeachDoLogStep,
    MainForeachStepInputForeachDoEmbedStep,
    MainForeachStepInputForeachDoSearchStep,
]

_MainForeachStepInputForeachReservedKeywords = TypedDict(
    "_MainForeachStepInputForeachReservedKeywords",
    {
        "in": str,
    },
    total=False,
)


class MainForeachStepInputForeach(_MainForeachStepInputForeachReservedKeywords, total=False):
    do: Required[MainForeachStepInputForeachDo]


class MainForeachStepInput(TypedDict, total=False):
    foreach: Required[MainForeachStepInputForeach]


class MainParallelStepInputParallelEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainParallelStepInputParallelToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1Content(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(
    TypedDict, total=False
):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(
    TypedDict, total=False
):
    image_url: Required[
        MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL
    ]
    """The image URL"""

    type: Literal["image_url"]


MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainParallelStepInputParallelPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainParallelStepInputParallelPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainParallelStepInputParallelPromptStepInputPromptUnionMember0(
    _MainParallelStepInputParallelPromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[
            List[str], Iterable[MainParallelStepInputParallelPromptStepInputPromptUnionMember0ContentUnionMember1], str
        ]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainParallelStepInputParallelPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainParallelStepInputParallelPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainParallelStepInputParallelGetStep(TypedDict, total=False):
    get: Required[str]


class MainParallelStepInputParallelSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainParallelStepInputParallelLogStep(TypedDict, total=False):
    log: Required[str]


class MainParallelStepInputParallelEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainParallelStepInputParallelEmbedStep(TypedDict, total=False):
    embed: Required[MainParallelStepInputParallelEmbedStepEmbed]


class MainParallelStepInputParallelSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainParallelStepInputParallelSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainParallelStepInputParallelSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainParallelStepInputParallelSearchStepSearch: TypeAlias = Union[
    MainParallelStepInputParallelSearchStepSearchVectorDocSearchRequest,
    MainParallelStepInputParallelSearchStepSearchTextOnlyDocSearchRequest,
    MainParallelStepInputParallelSearchStepSearchHybridDocSearchRequest,
]


class MainParallelStepInputParallelSearchStep(TypedDict, total=False):
    search: Required[MainParallelStepInputParallelSearchStepSearch]


MainParallelStepInputParallel: TypeAlias = Union[
    MainParallelStepInputParallelEvaluateStep,
    MainParallelStepInputParallelToolCallStep,
    MainParallelStepInputParallelPromptStepInput,
    MainParallelStepInputParallelGetStep,
    MainParallelStepInputParallelSetStep,
    MainParallelStepInputParallelLogStep,
    MainParallelStepInputParallelEmbedStep,
    MainParallelStepInputParallelSearchStep,
]


class MainParallelStepInput(TypedDict, total=False):
    parallel: Required[Iterable[MainParallelStepInputParallel]]


class MainMainInputMapEvaluateStep(TypedDict, total=False):
    evaluate: Required[Dict[str, str]]


class MainMainInputMapToolCallStep(TypedDict, total=False):
    tool: Required[str]

    arguments: Union[Dict[str, str], Literal["_"]]


class MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1Content(TypedDict, total=False):
    text: Required[str]

    type: Literal["text"]


class MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL(TypedDict, total=False):
    url: Required[str]

    detail: Literal["low", "high", "auto"]


class MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel(TypedDict, total=False):
    image_url: Required[MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModelImageURL]
    """The image URL"""

    type: Literal["image_url"]


MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1: TypeAlias = Union[
    MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1Content,
    MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1ContentModel,
]

_MainMainInputMapPromptStepInputPromptUnionMember0ReservedKeywords = TypedDict(
    "_MainMainInputMapPromptStepInputPromptUnionMember0ReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class MainMainInputMapPromptStepInputPromptUnionMember0(
    _MainMainInputMapPromptStepInputPromptUnionMember0ReservedKeywords, total=False
):
    content: Required[
        Union[List[str], Iterable[MainMainInputMapPromptStepInputPromptUnionMember0ContentUnionMember1], str]
    ]

    role: Required[Literal["user", "assistant", "system", "function", "function_response", "function_call", "auto"]]

    name: Optional[str]


class MainMainInputMapPromptStepInput(TypedDict, total=False):
    prompt: Required[Union[Iterable[MainMainInputMapPromptStepInputPromptUnionMember0], str]]

    settings: Optional[ChatSettingsParam]


class MainMainInputMapGetStep(TypedDict, total=False):
    get: Required[str]


class MainMainInputMapSetStep(TypedDict, total=False):
    set: Required[Dict[str, str]]


class MainMainInputMapLogStep(TypedDict, total=False):
    log: Required[str]


class MainMainInputMapEmbedStepEmbed(TypedDict, total=False):
    text: Required[Union[str, List[str]]]


class MainMainInputMapEmbedStep(TypedDict, total=False):
    embed: Required[MainMainInputMapEmbedStepEmbed]


class MainMainInputMapSearchStepSearchVectorDocSearchRequest(TypedDict, total=False):
    vector: Required[Iterable[float]]

    confidence: float

    lang: Literal["en-US"]

    limit: int


class MainMainInputMapSearchStepSearchTextOnlyDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    lang: Literal["en-US"]

    limit: int


class MainMainInputMapSearchStepSearchHybridDocSearchRequest(TypedDict, total=False):
    text: Required[str]

    vector: Required[Iterable[float]]

    alpha: float

    confidence: float

    lang: Literal["en-US"]

    limit: int


MainMainInputMapSearchStepSearch: TypeAlias = Union[
    MainMainInputMapSearchStepSearchVectorDocSearchRequest,
    MainMainInputMapSearchStepSearchTextOnlyDocSearchRequest,
    MainMainInputMapSearchStepSearchHybridDocSearchRequest,
]


class MainMainInputMapSearchStep(TypedDict, total=False):
    search: Required[MainMainInputMapSearchStepSearch]


MainMainInputMap: TypeAlias = Union[
    MainMainInputMapEvaluateStep,
    MainMainInputMapToolCallStep,
    MainMainInputMapPromptStepInput,
    MainMainInputMapGetStep,
    MainMainInputMapSetStep,
    MainMainInputMapLogStep,
    MainMainInputMapEmbedStep,
    MainMainInputMapSearchStep,
]


class MainMainInput(TypedDict, total=False):
    map: Required[MainMainInputMap]

    over: Required[str]

    initial: object

    parallelism: Optional[int]

    reduce: Optional[str]


Main: TypeAlias = Union[
    MainEvaluateStep,
    MainToolCallStep,
    MainPromptStepInput,
    MainGetStep,
    MainSetStep,
    MainLogStep,
    MainEmbedStep,
    MainSearchStep,
    MainReturnStep,
    MainSleepStep,
    MainErrorWorkflowStep,
    MainYieldStep,
    MainWaitForInputStep,
    MainIfElseWorkflowStepInput,
    MainSwitchStepInput,
    MainForeachStepInput,
    MainParallelStepInput,
    MainMainInput,
]
