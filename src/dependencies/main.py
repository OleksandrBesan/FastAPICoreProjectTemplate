from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration
from core.utils.traceId import TraceIdExtractor

container = Container()

Provide = FastApiIntegration(container).depends

container[TraceIdExtractor] = TraceIdExtractor
