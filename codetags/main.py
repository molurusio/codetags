#!/usr/bin/env python

import os
from misc import misc

DEFAULT_NAMESPACE = "CODETAGS"

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
    if isinstance(descriptors, list):
      # filter valid descriptors
      def filter_descriptors(descriptor):
        if isinstance(descriptor, str):
          return True
        if isinstance(descriptor, dict) and "name" in descriptor:
          if "plan" in descriptor:
            plan = descriptor["plan"]
            if isinstance(plan, dict) and "enabled" in plan and isinstance(plan["enabled"], bool):
              if "version" in self.__presets:
                _validated = True
                _satisfied = True
                if "minBound" in plan and isinstance(plan["minBound"], str):
                  _validated = _validated and misc.isVersionValid(plan["minBound"])
                  if _validated:
                    _satisfied = _satisfied and misc.isVersionLTE(plan["minBound"], self.__presets["version"])
                    pass
                if "maxBound" in plan and isinstance(plan["maxBound"], str):
                  _validated = _validated and misc.isVersionValid(plan["maxBound"])
                  if _validated:
                    _satisfied = _satisfied and misc.isVersionLT(self.__presets["version"], plan["maxBound"])
                    pass
                if _validated:
                  if _satisfied:
                    return plan["enabled"]
                  else:
                    if "enabled" in descriptor and isinstance(descriptor["enabled"], bool):
                      return descriptor["enabled"]
                    return not plan["enabled"]
        pass
      refs = filter(filter_descriptors, descriptors)
      # extract tag labels
      def map_descriptors(descriptor):
        if isinstance(descriptor, str):
          return descriptor
        if isinstance(descriptor, dict) and "name" in descriptor:
          return descriptor["name"]
        return None
      tags = map(map_descriptors, refs)
      # add to declaredTags
      for tag in tags:
        if not tag in self.__store["declaredTags"]:
          self.__store["declaredTags"].append(tag)
      pass
    return self

  def isActive(self, *tagexps):
    pass
  
  def clearCache(self):
    self.__store["cachedTags"].clear()
    self._refreshEnv()
    return self
  
  def reset(self):
    self.clearCache()
    self.__store["declaredTags"].clear()
    self.__presets.clear()
    return self

  def _refreshEnv(self):
    self.__store["env"].clear()
    for tagType in ["includedTags", "excludedTags"]:
      self.__store[tagType] = self._getEnv(self._getLabel(tagType));
    return self
  
  def _getLabel(self, tagType):
    _label = '_'
    if "namespace" in self.__presets and isinstance(self.__presets["namespace"], str):
      _label = self.__presets["namespace"] + _label
    else:
      _label = DEFAULT_NAMESPACE + _label
    if tagType == "includedTags":
      return _label + ("INCLUDED_TAGS" if not "includedTagsLabel" in self.__presets else self.__presets["includedTagsLabel"])
    if tagType == "excludedTags":
      return _label + ("EXCLUDED_TAGS" if not "excludedTagsLabel" in self.__presets else self.__presets["excludedTagsLabel"])
    return _label + (misc.labelify(tagType) if not tagType in self.__presets else self.__presets[tagType])

  def _getEnv(self, label, defaultValue):
    # label is not a string
    if not isinstance(label, str):
      return None
    # environment variable has been cached
    if label in self.__store["env"]:
      return self.__store["env"][label]
    # determine environment value
    self.__store["env"][label] = None
    if isinstance(defaultValue, str):
      self.__store["env"][label] = defaultValue
    environValue = os.environ.get(label)
    if isinstance(environValue, str):
      self.__store["env"][label] = environValue
    # convert string to list
    self.__store["env"][label] = misc.stringToArray(self.__store["env"][label])
    return self.__store["env"][label]

  def getDeclaredTags(self):
    return self._cloneTags("declaredTags")

  def getExcludedTags(self):
    return self._cloneTags("excludedTags")

  def getIncludedTags(self):
    return self._cloneTags("includedTags")

  def _cloneTags(self, tagType):
    if tagType in self.__store:
      return self.__store[tagType][0::]
    return []

default = Codetags()

def newInstance(name, **kwargs):
  pass

def getInstance(name, **kwargs):
  pass
