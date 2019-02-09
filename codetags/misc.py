import logging

class Misc(object):
  _handler = logging.StreamHandler()

  def __init__(self):
    self._handler.setLevel(logging.DEBUG)
    self._handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

  def getLogger(self, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(self._handler)
    return logger

misc = Misc()
