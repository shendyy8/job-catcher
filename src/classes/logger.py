from loguru import logger
import sys

class Logger():

  def __init__(self):
    logger.remove()
    logger.add(sys.stdout,level="INFO")
    self._logger = logger

  def get_logger(self):
    return self._logger


