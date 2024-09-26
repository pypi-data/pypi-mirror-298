from typing import Callable, Dict, List, Optional, Any, Type, Union, Tuple
import http.server
import socketserver
from .routing.router import Router
from .ctx import request_context
from .request import Request
from .response import Response
from .exceptions import (
    HTTPException,
    NotFound,
    MethodNotAllowed,
    InternalServerError,
)

class Haru:
    def __init__(self, import_name: str):
        self.import_name: str = import_name
        self.router: Router = Router()

    def route(self, path: str, methods: Optional[List[str]] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.router.add_route(path, func, methods)
            return func
        return decorator

    def run(self, host: str = '127.0.0.1', port: int = 8000) -> None:
        handler_class = self._make_handler()
        with socketserver.ThreadingTCPServer((host, port), handler_class) as httpd:
            print(f"Serving on {host}:{port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Server is shutting down.")
                httpd.server_close()

    def _make_handler(self) -> Type[http.server.BaseHTTPRequestHandler]:
        app = self

        class RequestHandler(http.server.BaseHTTPRequestHandler):
            server_version = "HaruHTTP/0.1"

            def do_GET(self) -> None:
                self._handle_request()

            def do_POST(self) -> None:
                self._handle_request()

            def do_PUT(self) -> None:
                self._handle_request()

            def do_DELETE(self) -> None:
                self._handle_request()

            def do_PATCH(self) -> None:
                self._handle_request()

            def do_HEAD(self) -> None:
                self._handle_request()

            def do_OPTIONS(self) -> None:
                self._handle_request()

            def _handle_request(self) -> None:
                method = self.command
                path = self.path
                try:
                    handler, kwargs, allowed_methods = app.router.match(path, method)
                    if handler is not None:
                        req = Request(
                            method=method,
                            path=path,
                            headers=dict(self.headers)
                        )
                        token = request_context.set(req)
                        try:
                            response = handler(**kwargs)
                            # ここから変更
                            if isinstance(response, Response):
                                self._send_response(response)
                            elif isinstance(response, tuple):
                                if len(response) == 2:
                                    body, status_code = response
                                    response_obj = Response(body, status_code)
                                    self._send_response(response_obj)
                                else:
                                    raise TypeError("View function must return 'Response', 'str', or '(str, int)'")
                            elif isinstance(response, str):
                                self._send_response(Response(response))
                            else:
                                raise TypeError("View function must return 'Response', 'str', or '(str, int)'")
                            # ここまで変更
                        finally:
                            request_context.reset(token)
                    else:
                        if method == 'OPTIONS':
                            allowed_methods = set(allowed_methods)
                            if allowed_methods:
                                self.send_response(200)
                                self.send_header('Allow', ', '.join(sorted(allowed_methods)))
                                self.end_headers()
                            else:
                                raise NotFound("Not Found")
                        elif allowed_methods:
                            raise MethodNotAllowed(allowed_methods)
                        else:
                            raise NotFound("Not Found")
                except HTTPException as e:
                    self.send_response(e.status_code)
                    for key, value in e.headers.items():
                        self.send_header(key, value)
                    self.end_headers()
                    if self.command != 'HEAD' and e.status_code >= 400 and e.status_code != 204:
                        self.wfile.write(str(e).encode('utf-8'))
                except Exception as e:
                    self.send_error(500, str(e))

            def _send_response(self, response: Response) -> None:
                self.send_response(response.status_code)
                for key, value in response.headers.items():
                    self.send_header(key, value)
                self.end_headers()
                if self.command != 'HEAD' and response.status_code != 204:
                    self.wfile.write(response.get_content())

            def log_message(self, format: str, *args: Any) -> None:
                pass

        return RequestHandler
