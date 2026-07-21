import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONSOLE = logging.StreamHandler()
CONSOLE.setLevel(logging.INFO)

__CONSOLE_FORMAT = logging.Formatter("%(levelname)s - %(message)s")
CONSOLE.setFormatter(__CONSOLE_FORMAT)

__FILE_HANDLER = logging.FileHandler("app.log")
__FILE_HANDLER.setLevel(logging.DEBUG)

FILE_FORMAT = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
__FILE_HANDLER.setFormatter(FILE_FORMAT)

logger.addHandler(CONSOLE)
logger.addHandler(__FILE_HANDLER)
