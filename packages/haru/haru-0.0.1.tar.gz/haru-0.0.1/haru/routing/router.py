from typing import Callable, Dict, List, Optional, Tuple, Any
import re


class Route:
    def __init__(self, path: str, handler: Callable, methods: List[str]):
        self.path: str = path
        self.handler: Callable = handler
        self.methods: List[str] = methods
        self.pattern: re.Pattern = re.compile(f'^{path}$')

    def match(self, path: str) -> Optional[Dict[str, Any]]:
        match = self.pattern.match(path)
        if match:
            return match.groupdict()
        return None


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, path: str, handler: Callable, methods: Optional[List[str]] = None) -> None:
        methods = methods or ['GET']
        methods = [method.upper() for method in methods]

        # 'GET' が存在する場合、自動的に 'HEAD' を追加
        if 'GET' in methods and 'HEAD' not in methods:
            methods.append('HEAD')

        # 'OPTIONS' を自動的に追加
        if 'OPTIONS' not in methods:
            methods.append('OPTIONS')

        route = Route(path, handler, methods)
        self.routes.append(route)

    def match(self, path: str, method: str) -> Tuple[Optional[Callable], Dict[str, Any], List[str]]:
        allowed_methods: List[str] = []
        for route in self.routes:
            params = route.match(path)
            if params is not None:
                allowed_methods.extend(route.methods)
                if method in route.methods:
                    return route.handler, params, allowed_methods
        return None, {}, allowed_methods
