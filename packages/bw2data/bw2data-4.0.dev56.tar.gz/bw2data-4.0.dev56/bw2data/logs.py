import codecs
import datetime
import logging
import uuid
from logging.handlers import RotatingFileHandler

from bw2data import config, projects
from bw2data.utils import create_in_memory_zipfile_from_directory, random_string

try:
    import anyjson
except ImportError:
    anyjson = None


class FakeLog:
    """Like a log object, but does nothing"""

    def fake_function(cls, *args, **kwargs):
        return

    def __getattr__(self, attr):
        return self.fake_function


def get_logger(name, level=logging.INFO):
    filename = "{}-{}.log".format(
        name,
        datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p"),
    )
    handler = RotatingFileHandler(
        projects.logs_dir / filename,
        maxBytes=1e6,
        encoding="utf-8",
        backupCount=10,
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(lineno)d %(message)s")
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_io_logger(name):
    """Build a logger that records only relevent data for display later as HTML."""
    filepath = projects.logs_dir / "{}.{}.log".format(name, random_string(6))
    handler = logging.StreamHandler(codecs.open(filepath, "w", "utf-8"))
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger, filepath


def get_verbose_logger(name, level=logging.WARNING):
    filename = "{}-{}.log".format(
        name,
        datetime.datetime.now().strftime("%d-%B-%Y-%I-%M%p"),
    )
    handler = RotatingFileHandler(
        projects.logs_dir / filename,
        maxBytes=50000,
        encoding="utf-8",
        backupCount=5,
    )
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            """
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s
Message:
%(message)s

"""
        )
    )
    logger.addHandler(handler)
    return logger


def close_log(log):
    """Detach log handlers; flush to disk"""
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)
