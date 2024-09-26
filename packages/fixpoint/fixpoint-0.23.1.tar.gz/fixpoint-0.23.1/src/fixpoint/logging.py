"""Logging for the Fixpoint SDK."""

__all__ = ["CALLCACHE_LOGGER_NAME", "logger", "callcache_logger", "fc_logger"]

import logging

LOGGER_NAME = "fixpoint"
CALLCACHE_LOGGER_NAME = "fixpoint.workflows.structured._callcache"

logger = logging.getLogger(LOGGER_NAME)
callcache_logger = logger.getChild(CALLCACHE_LOGGER_NAME)
fc_logger = logger.getChild("fc")
