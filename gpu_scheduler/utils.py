# Python stdlib
import logging

# Project Dependencies
# Project Imports


def configure_logger():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("[%(levelname)s] - %(asctime)s - : %(message)s")

    logger.setLevel(logging.ERROR)

    fh = logging.FileHandler("scheduler.log", mode="w")
    fh.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(sh)
        logger.addHandler(fh)

    return logger


if __name__ == "__main__":
    pass
