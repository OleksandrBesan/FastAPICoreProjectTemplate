from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
import asyncpg
from urllib.parse import quote
from core.settings.app import AppSettings
from dependencies.main import Provide
from collections.abc import AsyncIterator


@asynccontextmanager
async def postgresql_lifespan(
    app: FastAPI, 
    settings: AppSettings = Provide(AppSettings)
)  -> AsyncIterator[None]:
    def create_db_connection_url(secrets): 
        encoded_password = quote(secrets['password'])
        return f"postgresql://{secrets['username']}:{encoded_password}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
    logger.info("Connecting to PostgreSQL")
    try:
        app.state.pool = await asyncpg.create_pool(
            str(create_db_connection_url(settings.DB_POSTGRESQL_URL_PARAMS)),
            min_size=settings.DB_POSTGRESQL_MIN_CONNECTION,
            max_size=settings.DB_POSTGRESQL_MAX_CONNECTION,
        )
    except Exception as e:
        logger.error("Connection to PostgreSQL failed")
        logger.error(e)
    else:
        logger.info("Connection to PostgreSQL established")
    yield
    logger.info("Closing connection to PostgreSQL")
    await app.state.pool.close()
    logger.info("Connection to PostgreSQL closed")
