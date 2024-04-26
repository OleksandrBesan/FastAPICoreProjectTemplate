from fastapi import APIRouter, Request
from loguru import logger

from api.schemas.test import SomeRequestModel, SomeResponseModel
from core.settings.app import AppSettings
from core.utils.traceId import TraceIdExtractor
from core.utils.logging import LoggingRoute
from core.exceptions.api import BadRequestException, InternalServerException
from dependencies.main import Provide
router = APIRouter(
    tags=['test'],
    route_class=LoggingRoute
)


@router.post("/test/dosomething"
             , summary="test endnpoint to do something"
             , responses={200: {"model": SomeRequestModel, "description": "Successful result"},
                          400: {"model": BadRequestException.model, "description": str(BadRequestException)},
                          500: {"model": InternalServerException.model, "description": str(InternalServerException)}
                          })
async def do_something(request: Request,
                       input_data: SomeRequestModel,
                       settings: AppSettings = Provide(AppSettings),
                       trace: TraceIdExtractor = Provide(TraceIdExtractor)):
    """
       test
    """
    route_path = request.url.path
    traceId = trace.getTraceId()
    with logger.contextualize(traceId=traceId, path=route_path):
        response = SomeResponseModel(result=True, traceId=traceId)
        return response
