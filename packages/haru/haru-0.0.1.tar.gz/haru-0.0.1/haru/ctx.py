import contextvars
from typing import Any

request_context: contextvars.ContextVar[Any] = contextvars.ContextVar('request_context')
