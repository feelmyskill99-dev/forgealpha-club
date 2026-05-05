import logging

import structlog

from app.core.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
        if settings.ENV == "production"
        else structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(settings.LOG_LEVEL)),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
