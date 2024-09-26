from typing import Any, Dict


class Response:
    def __init__(self, content: Any, status_code: int = 200, headers: Dict[str, str] = None):
        self.content: Any = content
        self.status_code: int = status_code
        self.headers: Dict[str, str] = headers or {}

    def get_content(self) -> bytes:
        if isinstance(self.content, bytes):
            return self.content
        elif isinstance(self.content, str):
            return self.content.encode('utf-8')
        else:
            raise TypeError("Response content must be str or bytes")
