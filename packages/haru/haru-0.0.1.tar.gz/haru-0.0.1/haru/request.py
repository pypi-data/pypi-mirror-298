from typing import Any
from .ctx import request_context


class Request:
    def __init__(self, method: str, path: str, headers: dict):
        self.method: str = method
        self.path: str = path
        self.headers: dict = headers
        # 必要に応じて他の属性を追加


class RequestProxy:
    def __getattr__(self, name: str) -> Any:
        req = request_context.get()
        return getattr(req, name)


request = RequestProxy()
