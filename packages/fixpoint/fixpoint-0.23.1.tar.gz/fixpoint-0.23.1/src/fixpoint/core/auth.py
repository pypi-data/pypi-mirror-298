"""Utilities for working with requests and authentication"""

__all__ = ["new_api_key_header"]

from typing import Dict


def new_api_key_header(api_key: str) -> Dict[str, str]:
    """Create a new API key header"""
    return {"API-Key": api_key}
