# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EnrichCreateParams"]


class EnrichCreateParams(TypedDict, total=False):
    email: str
    """The person's business email address.

    We won't accept personal email address such as Gmail, Yahoo etc.
    """
