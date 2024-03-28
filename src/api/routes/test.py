from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
import traceback

from api.models.SomeRequestModel import SomeRequestModel
from api.models.SomeResponseModel import SomeResponseModel
from api.models.ErrorResponseModel import ErrorResponseModel
from core.settings.app import AppSettings
from core.config import get_app_settings
from core.utils.requestId import getRequestId
from api.routes.logging import LoggingRoute
router = APIRouter(
    tags=['test'],
    route_class=LoggingRoute
)


@router.post("/test/dosomething"
             , summary="test endnpoint to do something"
             , responses={200: {"model": SomeRequestModel, "description": "Successful result"},
                          400: {"model": ErrorResponseModel, "description": "Bad Request"},
                          500: {"model": ErrorResponseModel, "description": "Internal Server Error"}})
async def do_something(request: Request,
                       input_data: SomeRequestModel,
                       settings: AppSettings = Depends(get_app_settings),
                       requestId: str = Depends(getRequestId)):
    """
       test
    """
    route_path = request.url.path
    with logger.contextualize(requestId=requestId, path=route_path):
        try:
            response = SomeResponseModel(result=True)
            return response
        except Exception as e:
            tb_str = traceback.format_exc()
            logger.error(tb_str)
            raise HTTPException(status_code=500, detail=ErrorResponseModel(
                error_code=500,
                error_message=str(e)
            ))
