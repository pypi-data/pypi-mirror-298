LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(message)s",
            "datefmt": "%X",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "default",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "aiortc": {"level": "INFO", "propagate": False, "handlers": ["console"]},
        "whipweb": {"level": "DEBUG", "propagate": False, "handlers": ["console"]},
        "uvicorn": {"level": "INFO", "propagate": False, "handlers": ["console"]},
    },
}
