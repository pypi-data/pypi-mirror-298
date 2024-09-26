"""Constants for the Fixpoint package"""

__all__ = [
    "TASK_MAIN_ID",
    "STEP_MAIN_ID",
    "NULL_COL_ID",
    "API_BASE_URL",
    "NO_AUTH_ORG_ID",
    "NO_AUTH_USER_ID",
    "NO_AUTH_AUTH_TOKEN",
]

TASK_MAIN_ID = "__main__"
STEP_MAIN_ID = "__main__"

TASK_CLOSED_ID = "__closed__"
STEP_CLOSED_ID = "__closed__"

NULL_COL_ID = "__null__"

API_BASE_URL = "https://apiv1.fixpoint.co"

NO_AUTH_ORG_ID = "org-__NO_AUTH__"
NO_AUTH_USER_ID = "user-__NO_AUTH__"
NO_AUTH_AUTH_TOKEN = "token-__NO_AUTH__"

DEFAULT_API_CLIENT_TIMEOUT = 10.0
