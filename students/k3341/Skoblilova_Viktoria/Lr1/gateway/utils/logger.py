"""Корневой логгер API: уровень из настроек, вывод в stdout."""

import logging
import sys
from config import app_settings

logger = logging.getLogger("api")
logger.setLevel(getattr(logging, app_settings.LOGLEVEL))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, app_settings.LOGLEVEL))

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)