# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .shared_params.sampling_params import SamplingParams

__all__ = ["InferenceCompletionParams", "Logprobs"]


class InferenceCompletionParams(TypedDict, total=False):
    content: Required[Union[str, List[str]]]

    model: Required[str]

    logprobs: Logprobs

    sampling_params: SamplingParams

    stream: bool

    x_llama_stack_provider_data: Annotated[str, PropertyInfo(alias="X-LlamaStack-ProviderData")]


class Logprobs(TypedDict, total=False):
    top_k: int
