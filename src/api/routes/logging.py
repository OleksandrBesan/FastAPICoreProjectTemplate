from fastapi import Response, Request
from fastapi.routing import APIRoute
from starlette.responses import StreamingResponse
from core.config import get_app_settings
from core.logging import logcontext, LogTimerContext
from core.utils.url import parse_url
from core.exceptions.base import BaseHTTPException
from typing import Callable
from loguru import logger
from io import BytesIO
import json


class LoggingRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        settings = get_app_settings()
        header_name_requestId = settings.header_name_requestId
        logging_request_headers = settings.logging_request_headers
        restrictRoutes = settings.logging_request_restrict_routes_with_keys.routes
        filterKeys = settings.logging_request_restrict_routes_with_keys.filter_keys
        maskKeys = settings.logging_request_restrict_routes_with_keys.mask_keys
        logging_response_filter = settings.logging_response_filter

        route_logger = logger.bind()

        async def process_request_body(req_body, path, route_logger):
            if {"*"} & set(restrictRoutes) and {"*"} <= set(filterKeys) and {"*"} <= set(maskKeys):
                route_logger.bind(tag="RequestRaw").info(req_body)
            elif {"*", path} & set(restrictRoutes):
                try:
                    request_text = req_body.decode('utf-8')
                    request_headers = json.loads(request_text)
                    filtered_request = {key: (value if key not in maskKeys else "****") for key, value in request_headers.items() if key not in filterKeys}
                    route_logger.bind(tag="RequestFiltered").info(filtered_request)
                except Exception as e:
                    logger.error(e)
                    route_logger.bind(tag="RequestRaw").info(req_body)

        async def log_request(request: Request, route_logger):
            requestId = request.headers.get(header_name_requestId, None)
            _, path = parse_url(str(request.url))
            self.requestId = requestId
            self.requestPath = path
            route_logger = route_logger.bind(requestId=requestId, path=path, tag="RequestHeaders")
            request_headers_json = {key: value for key, value in request.headers.items() if key in logging_request_headers or "*" in logging_response_filter}
            route_logger.info(json.dumps(request_headers_json))

            req_body = await request.body()
            await process_request_body(req_body, path, route_logger)

        async def log_response(response: Response, route_logger):
            route_logger = route_logger.bind(requestId=self.requestId, path=self.requestPath, tag="ResponseRaw")
            buffer = BytesIO()
            if isinstance(response, StreamingResponse):
                async for item in response.body_iterator:
                    if isinstance(item, str):
                        item = item.encode('utf-8')
                    buffer.write(item)
            else:
                buffer.write(response.body)
            res_body = buffer.getvalue()
            buffer.close()
            response_text = res_body.decode('utf-8')
            try:
                response_dict = json.loads(response_text)
                filtered_response = {key: value for key, value in response_dict.items() if key in logging_response_filter or "*" in logging_response_filter}
                route_logger.info(filtered_response)
            except json.JSONDecodeError:
                # for now without handling non json
                pass

            return Response(content=res_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)

        @logcontext(tag="RequestRaw")
        async def route_handler(request: Request) -> Response:
            await log_request(request, route_logger)

            try:
                with LogTimerContext(logger=route_logger.bind(requestId=self.requestId, path=self.requestPath, tag='performanceResponse')):
                    response = await original_route_handler(request)
            except BaseHTTPException as exc:
                response = exc.response(requestId=self.requestId)

            return await log_response(response, route_logger)

        return route_handler
