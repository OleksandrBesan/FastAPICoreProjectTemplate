import logging
from logging.config import dictConfig 
class CorrelationIdLoggingFilter(logging.Filter):
    """
    Logging filter to inject traceId into log records.
    """
    def filter(self, record):
        print(record)
        return True

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s]|[guvicorn]|[%(filename)s]|[]|[]|[]|[%(process)s]|[%(levelname)s]|[%(module)s - %(name)s:%(lineno)d] - [%(message)s]]', 
            'datefmt': '%Y-%m-%dT%H:%M:%S.0%z',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {   
            'handlers': ['console'],
            'level': 'INFO',
        },
        'gunicorn.error': {   
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'gunicorn.access': {  
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'uvicorn.error': { 
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'uvicorn.access': { 
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Apply the logging configuration
dictConfig(LOGGING_CONFIG)
raw_env = [
    "UVICORN_LOGGING_CONFIG=config.json",
]
logconfig_dict = LOGGING_CONFIG
bind = "0.0.0.0:8000"
workers=3
graceful_timeout=100
timeout=150
keep_alive=150
