import sys
import logging

logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def getLog():
    """simple wrapper around basic logger"""
    return logging
