#!/usr/bin/env python

from misc import misc

class Codetags(object):
  def __init__(self, **kwargs):
    self.__store = {
      "env": {},
      "cachedTags": {},
      "declaredTags": []
    }
    self.__presets = {}
    self.initialize()
    pass

  def initialize(self, **kwargs):
    for field_name in ["namespace", "includedTagsLabel", "excludedTagsLabel"]:
      if field_name in kwargs and type(kwargs[field_name]) == str:
        self.__presets[field_name] = misc.labelify(kwargs[field_name])
        pass
    for field_name in ["version"]:
      if field_name in kwargs and type(kwargs[field_name]) == str:
        self.__presets[field_name] = kwargs[field_name]
        pass
    return self

  def register(self, descriptors):
    pass

  def isActive(self, tagexp):
    pass
  
  def clearCache(self):
    pass
  
  def reset(self):
    pass

default = Codetags()

def newInstance(name, **kwargs):
  pass

def getInstance(name, **kwargs):
  pass
