from typing import Callable
from fastapi import Request as FastApiRequest, Response as FastApiResponse, FastAPI

from azfuncextbase import WebServer, WebApp, RequestTrackerMeta, ResponseTrackerMeta
import uvicorn

class Request(metaclass=RequestTrackerMeta):
    request_type = FastApiRequest

class Response(metaclass=ResponseTrackerMeta):
    response_type = FastApiResponse


class WebApp(WebApp):
    def __init__(self):
        self.web_app = FastAPI()

    def route(self, func: Callable):
        # Apply the api_route decorator
        decorated_function = self.web_app.api_route(
            "/{path:path}",
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]
        )(func)

        return decorated_function

    def get_app(self):
        return self.web_app
    

class WebServer(WebServer):
    async def serve(self):
        uvicorn_config = uvicorn.Config(self.web_app, host=self.hostname, port=self.port)
    
        server = uvicorn.Server(uvicorn_config)

        return await server.serve()


# app = WebApp()

# @app.route
# async def catch_all(request):
#     return "hello"

# print(app.get_app().routes)
# print(RequestTrackerMeta.get_request_type())