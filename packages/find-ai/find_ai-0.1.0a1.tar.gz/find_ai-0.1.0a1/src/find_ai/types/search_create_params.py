# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SearchCreateParams"]


class SearchCreateParams(TypedDict, total=False):
    max_matches: float
    """The maximum number of results to return. optional for result_mode exact"""

    query: str
    """Search query."""

    result_mode: str
    """The mode of the search. Valid values are 'exact' or 'best'."""

    scope: str
    """The scope of the search. Valid values are 'people' or 'companies'."""
