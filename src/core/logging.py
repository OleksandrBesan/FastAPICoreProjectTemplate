import logging
from types import FrameType
from typing import cast

import asyncio
from loguru import logger
import functools
import traceback
from timeit import default_timer as timer
from datetime import timedelta
from contextlib import ContextDecorator


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = cast(FrameType, frame.f_back)
            depth += 1


def logcontext(**context_vars):
    """
    decorator to imply to the call func contextualize with provided tags
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    with logger.contextualize(**context_vars):
                        return await func(*args, **kwargs)
                except Exception as e:
                    with logger.contextualize(**context_vars):
                        logger.error(traceback.format_exc().replace('\n', '\\n'))
                    raise e

            return async_wrapper

        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    with logger.contextualize(**context_vars):
                        return func(*args, **kwargs)
                except Exception as e:
                    with logger.contextualize(**context_vars):
                        logger.error(traceback.format_exc().replace('\n', '\\n'))
                    raise e
            return sync_wrapper
    return decorator


def logtimer(tag="performance"):
    """
    decorator to log performance of the call func with contextualize
    Provided requestPath, requestId on the self of the method
    (if decorator on the class)
    """
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            requestId = getattr(args[0], 'requestId', '')
            requestPath = getattr(args[0], 'requestPath', '')
            decorator_logger = logger.bind(
                requestId=requestId,
                path=requestPath,
                tag=tag
            )
            start = timer()
            result = func(*args, **kwargs)
            end = timer()
            logtext = f"Execution time: {timedelta(seconds=end-start)}"
            decorator_logger.info(logtext)
            return result

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            requestId = getattr(args[0], 'requestId', '')
            requestPath = getattr(args[0], 'requestPath', '')
            decorator_logger = logger.bind(
                requestId=requestId,
                path=requestPath,
                tag=tag
            )
            start = timer()
            result = await func(*args, **kwargs)
            end = timer()
            logtext = f"Execution time: {timedelta(seconds=end-start)}"
            decorator_logger.info(logtext)
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


class LogTimerContext(ContextDecorator):
    """
    context manager to log time of the block
    Accept logger, with necessary binding
    """
    def __init__(self, logger):
        self.logger = logger
        self.start_time = None

    def __enter__(self):
        self.start_time = timer()
        return self

    def __exit__(self, *exc):
        end_time = timer()
        start_time = self.start_time
        elapsed_time = timedelta(seconds=end_time - start_time)
        self.logger.info(f"Execution time: {elapsed_time}")
        return False
