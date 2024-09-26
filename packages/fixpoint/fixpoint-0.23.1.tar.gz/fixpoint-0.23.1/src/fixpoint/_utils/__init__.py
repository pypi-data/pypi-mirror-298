"""
This module contains the utility functions and classes.
"""

__all__ = [
    "get_env_or_fail",
    "prefer_val_or_must_get_env",
    "decorate_instructor_completion_with_fixp",
]

import os
from typing import Optional

from fixpoint.errors import ConfigError
from .completions import decorate_instructor_completion_with_fixp


def prefer_val_or_must_get_env(
    key: str, preferred: Optional[str] = None, default: Optional[str] = None
) -> str:
    """Get an environment variable or fail"""
    if preferred is not None:
        return preferred
    return get_env_or_fail(key, default)


def get_env_or_fail(key: str, default: Optional[str] = None) -> str:
    """Get an environment variable or fail"""
    value = os.environ.get(key, default)
    if value is None:
        raise ConfigError(f"Environment variable {key} is not set")
    return value
