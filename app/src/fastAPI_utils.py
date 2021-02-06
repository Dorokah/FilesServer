import time
from collections import Callable
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from h11 import Response
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from src.config_provider import get_config

config = get_config()


def create_app():
    rest_app = FastAPI(title='Magma Image Bank',
                       description="an app to store and serve images.",
                       version="beta", docs_url=None, redoc_url=None, debug=False)
    rest_app.mount("/static", StaticFiles(directory="static"), name="static")

    @rest_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(swagger_favicon_url="/static/favicon.ico", openapi_url=rest_app.openapi_url,
                                   title=rest_app.title, swagger_css_url="/static/swagger-ui.css",
                                   oauth2_redirect_url=rest_app.swagger_ui_oauth2_redirect_url,
                                   swagger_js_url="/static/swagger-ui-bundle.js")

    @rest_app.get(rest_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @rest_app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(openapi_url=rest_app.openapi_url,
                              title=rest_app.title + " - ReDoc",
                              redoc_js_url="/static/redoc.standalone.js")

    def custom_openapi():
        if rest_app.openapi_schema:
            return rest_app.openapi_schema
        openapi_schema = get_openapi(title=config['appName'],
                                     description=config['appDescription'],
                                     version=config['appVersion'],
                                     routes=rest_app.routes)
        openapi_schema["info"]["x-logo"] = {"url": "/static/parallax_logo_magma.jpg"}
        rest_app.openapi_schema = openapi_schema
        return rest_app.openapi_schema

    rest_app.openapi = custom_openapi
    return rest_app


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            response.headers["X-Response-Time"] = str(time.time() - before)
            return response

        return custom_route_handler
