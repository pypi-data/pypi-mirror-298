# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["EnrichCreateResponse"]


class EnrichCreateResponse(BaseModel):
    designation: str

    email: str

    facts: List[str]
    """A list of facts we have on record about the person."""

    first_name: str

    last_name: str

    name: str

    short_description: str
    """A summary of information about the person."""

    linkedin_url: Optional[str] = None
    """The URL to the person's LinkedIn profile if one exists."""

    photo_url: Optional[str] = None
    """A URL to the person's profile image obtained from LinkedIn.

    Valid for 10 minutes.
    """
