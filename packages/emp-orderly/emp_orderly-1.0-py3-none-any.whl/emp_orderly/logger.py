import os
import logging
import sys

logger = logging.getLogger(__name__)
fh = logging.FileHandler(os.environ.get("ERR_LOG_PATH", "err.log"))
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)


def log_to_stdout():
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.addHandler(fh)
    logger.setLevel(logging.ERROR)
