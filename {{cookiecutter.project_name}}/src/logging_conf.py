import atexit
import logging
import warnings
from logging.config import dictConfig
from typing import Any

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from src.settings import config


class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.is_valid:
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        return True


def setup_logging():
    warnings.filterwarnings(
        "ignore",
        message=".*Pydantic serializer warnings.*",
        category=UserWarning,
        module="pydantic.main",
    )

    filters = {
        "trace_context": {"()": TraceContextFilter},
    }

    handlers: dict[str, Any] = {
        "default": {
            "class": "logging.StreamHandler",
            "level": config.LOG_LEVEL,
            "formatter": "console",
            "filters": ["trace_context"],
        },
    }

    if config.OPEN_TELEMETRY_FLAG:
        resource = Resource.create({"service.name": config.SERVICE_NAME})

        tracer_provider = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer_provider)

        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)

        otel_headers = (
            {"Authorization": config.OPEN_TELEMETRY_AUTHORIZATION_TOKEN}
            if config.OPEN_TELEMETRY_AUTHORIZATION_TOKEN
            else None
        )

        trace_exporter = OTLPSpanExporter(
            endpoint=(
                config.OPEN_TELEMETRY_TRACE_ENDPOINT.unicode_string()
                if config.OPEN_TELEMETRY_TRACE_ENDPOINT
                else None
            ),
            headers=otel_headers,
        )
        tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

        log_exporter = OTLPLogExporter(
            endpoint=(
                config.OPEN_TELEMETRY_LOG_ENDPOINT.unicode_string()
                if config.OPEN_TELEMETRY_LOG_ENDPOINT
                else None
            ),
            headers=otel_headers,
        )
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        atexit.register(tracer_provider.shutdown)
        atexit.register(logger_provider.shutdown)

        handlers["otel"] = {
            "()": LoggingHandler,
            "level": config.LOG_LEVEL,
            "logger_provider": logger_provider,
            "filters": ["trace_context"],
        }

    formatters = {
        "console": {
            "class": "logging.Formatter",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
            "format": "%(asctime)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
        }
    }

    # Declare src logger as the root logger
    # Any other loggers will be children of src and inherit the settings
    loggers = {
        "src": {
            "level": config.LOG_LEVEL,
            "handlers": list(handlers.keys()),
            "propagate": False,
        }
    }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": formatters,
            "filters": filters,
            "handlers": handlers,
            "loggers": loggers,
        }
    )
