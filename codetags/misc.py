#!/usr/bin/env python

import logging
import re

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

  def labelify(self, label):
    if type(label) == str:
      return re.sub('\W{1,}', '_', label).upper()
    return label

  def stringToArray(self, labels):
    if isinstance(labels, str):
      _arr = re.split(r',', labels)
      def labels_map(item):
        return item.strip()
      def labels_filter(item):
        return len(item) > 0
      _arr = map(labels_map, _arr)
      _arr = filter(labels_filter, _arr)
      return _arr
    return []

misc = Misc()
