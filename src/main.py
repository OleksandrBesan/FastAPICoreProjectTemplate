from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import get_app_settings
from api.routes.main import router as api_router
from core.settings.env import ENV_PATH
from dotenv import load_dotenv
from loguru import logger
from uuid import uuid4
from asgi_correlation_id import CorrelationIdMiddleware
from core.exceptions.handlers import errorHandlers


def get_application() -> FastAPI:

    load_dotenv(ENV_PATH)

    settings = get_app_settings()

    settings.configure_logging()
    settings.configure_env()
    logger.info(settings.app_env)
    application = FastAPI(**settings.fastapi_kwargs)
    application.add_middleware(
        CorrelationIdMiddleware,
        header_name=settings.header_name_traceId,
        update_request_header=True,
        generator=lambda: uuid4().hex,
        transformer=lambda a: a,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=['X-Request-ID', settings.header_name_traceId]
    )
    application.include_router(api_router)
    return application


app = get_application()

for err, handler in errorHandlers:
    app.add_exception_handler(err, handler)

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn_app = f"{os.path.basename(__file__).removesuffix('.py')}:app"
    uvicorn.run(app, host="0.0.0.0", port=8000)
