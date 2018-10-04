__author__ = 'raphaelfettaya'
import logging


logging.basicConfig(level=logging.INFO)


def get_logger(name):
    return logging.getLogger(name)
