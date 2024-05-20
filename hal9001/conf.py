import logging

from .types.config import Settings

logging.basicConfig(level=logging.INFO, format="%(relativeCreated)6d %(threadName)s %(message)s")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")


__all__ = ["settings"]
