import structlog
import logging
from app.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(message)s",
)

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer() if settings.ENV == "production" else structlog.dev.ConsoleRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger("forgealpha")