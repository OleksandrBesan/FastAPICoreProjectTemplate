from fastapi import APIRouter, Depends, Request
from loguru import logger

from api.schemas.test import SomeRequestModel, SomeResponseModel
from core.settings.app import AppSettings
from core.config import get_app_settings
from core.utils.traceId import getTraceId
from core.utils.logging import LoggingRoute
from core.exceptions.api import BadRequestException, InternalServerException
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
                       settings: AppSettings = Depends(get_app_settings),
                       traceId: str = Depends(getTraceId)):
    """
       test
    """
    route_path = request.url.path
    with logger.contextualize(traceId=traceId, path=route_path):
        response = SomeResponseModel(result=True, traceId=traceId)
        return response
