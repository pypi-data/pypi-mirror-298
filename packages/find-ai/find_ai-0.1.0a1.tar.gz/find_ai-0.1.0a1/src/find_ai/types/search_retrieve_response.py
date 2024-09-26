# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["SearchRetrieveResponse", "SearchRetrieveResponseItem", "SearchRetrieveResponseItemCompany"]


class SearchRetrieveResponseItemCompany(BaseModel):
    name: str
    """Returned only for a person."""

    slug: str
    """Returned only for a person."""

    website: str
    """Returned only for a person."""


class SearchRetrieveResponseItem(BaseModel):
    linkedin_url: str

    name: str

    photo_url: str

    reason: str

    short_description: str

    slug: str

    company: Optional[SearchRetrieveResponseItemCompany] = None

    company_size: Optional[str] = None
    """Returned only for a company."""

    inferred_email: Optional[str] = None
    """Returned only for a person."""

    locations: Optional[List[str]] = None
    """Returned only for a company."""

    title: Optional[str] = None
    """Returned only for a person."""


SearchRetrieveResponse: TypeAlias = List[SearchRetrieveResponseItem]
