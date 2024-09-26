# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["EnrichCreateResponse"]


class EnrichCreateResponse(BaseModel):
    facts: List[str]
    """A list of facts we have on record about the company."""

    name: str

    short_description: str
    """A summary of information about the company."""

    website: str

    linkedin_url: Optional[str] = None
    """The URL to the company's LinkedIn profile if one exists."""

    photo_url: Optional[str] = None
    """A URL to an image of the company's logo. Valid for 10 minutes."""
