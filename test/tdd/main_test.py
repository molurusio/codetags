#!/usr/bin/env python

import unittest
from unittest_data_provider import data_provider
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../codetags')

from main import default as codetags
from main import newInstance

class CodetagsTest(unittest.TestCase):

  def setUp(self):
    pass
  
  def tearDown(self):
    codetags.reset()
    pass

  def test_invalid_instance_name(self):
    # with self.assertRaises(Exception) as context:
    #   newInstance(1024)
    # self.assertTrue('This is broken' in context.exception)
    pass

  def data_register_add_descriptors():
    return [
      ['0.1.0', ["feature-01", "feature-02", "feature-12"] ],
      ['0.1.3', ["feature-01", "feature-02", "feature-11", "feature-12"] ],
      ['0.2.2', ["feature-01", "feature-02", "feature-11", "feature-12", "feature-13"] ],
      ['0.2.8', ["feature-01", "feature-02", "feature-11"] ],
      ['0.2.9', ["feature-01", "feature-02", "feature-11", "feature-14"] ],
      ['0.2.10', ["feature-01", "feature-02", "feature-11", "feature-14"] ]
    ]

  @data_provider(data_register_add_descriptors)
  def test_register_add_descriptors(self, version, featureList):
    codetags.reset()
    codetags.initialize(**{
        'namespace': 'codetags',
        'positiveTagsLabel': 'INCLUDED_TAGS',
        'negativeTagsLabel': 'EXCLUDED_TAGS',
        'version': version,
    })
    codetags.register([
      'feature-01',
      {
        'name': 'feature-02'
      },
      {
        'name': 'feature-03',
        'enabled': False
      },
      {
        'name': 'feature-04',
        'plan': {
          'enabled': False
        }
      },
      {
        'name': 'feature-11',
        'plan': {
          'enabled': True,
          'minBound': '0.1.2'
        }
      },
      {
        'name': 'feature-12',
        'plan': {
          'enabled': True,
          'maxBound': '0.2.8'
        }
      },
      {
        'name': 'feature-13',
        'plan': {
          'enabled': True,
          'minBound': '0.2.1',
          'maxBound': '0.2.7'
        }
      },
      {
        'name': 'feature-14',
        'plan': {
          'enabled': False,
          'maxBound': '0.2.9'
        }
      },
    ])
    self.assertListEqual(codetags.getDeclaredTags(), featureList)
    pass

  def data_getLabel():
    return [
      [ None, "includedTags", None, "CODETAGS_INCLUDED_TAGS" ],
      [ None, "excludedTags", None, "CODETAGS_EXCLUDED_TAGS" ],
      [ None, "includedTags", "POSITIVE_TAGS", "CODETAGS_POSITIVE_TAGS" ],
      [ None, "excludedTags", "NEGATIVE_TAGS", "CODETAGS_NEGATIVE_TAGS" ],
      [ "testing", "includedTags", "POSITIVE_TAGS", "TESTING_POSITIVE_TAGS" ],
      [ "TESTING", "excludedTags", "NEGATIVE_TAGS", "TESTING_NEGATIVE_TAGS" ]
    ]

  @data_provider(data_getLabel)
  def test_getLabel(self, namespace, label_type, label, expected):
    _params = {}
    if isinstance(label, str):
      _params[label_type + 'Label'] = label
    if isinstance(namespace, str):
      _params["namespace"] = namespace
      pass
    codetags.reset().initialize(**_params)
    self.assertEquals(codetags._getLabel(label_type), expected)
    pass

  def test_isActive(self):
    os.environ["CODETAGS_INCLUDED_TAGS"] = "abc, def, xyz, tag-4"
    os.environ["CODETAGS_EXCLUDED_TAGS"] = "disabled, tag-2"
    codetags.reset().register(['tag-1', 'tag-2'])
    # An arguments-list presents the OR conditional operator
    self.assertTrue(codetags.isActive('abc'));
    self.assertTrue(codetags.isActive('abc', 'xyz'));
    self.assertTrue(codetags.isActive('abc', 'disabled'));
    self.assertTrue(codetags.isActive('disabled', 'abc'));
    self.assertTrue(codetags.isActive('abc', 'nil'));
    self.assertTrue(codetags.isActive('undefined', 'abc', 'nil'));
    self.assertFalse(codetags.isActive());
    self.assertFalse(codetags.isActive(None));
    self.assertFalse(codetags.isActive('disabled'));
    self.assertFalse(codetags.isActive('nil'));
    self.assertFalse(codetags.isActive('nil', 'disabled'));
    self.assertFalse(codetags.isActive('nil', 'disabled', 'abc.xyz'));
    # An array argument presents the AND conditional operator
    self.assertTrue(codetags.isActive(['abc', 'xyz'], 'nil'));
    self.assertTrue(codetags.isActive(['abc', 'xyz'], None));
    self.assertFalse(codetags.isActive(['abc', 'nil']));
    self.assertFalse(codetags.isActive(['abc', 'def', 'nil']));
    self.assertFalse(codetags.isActive(['abc', 'def', 'disabled']));
    self.assertFalse(codetags.isActive(['abc', '123'], ['def', '456']));
    # pre-defined tags are overridden by values of environment variables
    self.assertTrue(codetags.isActive('abc'));
    self.assertTrue(codetags.isActive('tag-1'));
    self.assertTrue(codetags.isActive('abc', 'tag-1'));
    self.assertTrue(codetags.isActive('disabled', 'tag-1'));
    self.assertTrue(codetags.isActive('tag-4'));
    self.assertFalse(codetags.isActive('tag-2'));
    self.assertFalse(codetags.isActive('tag-3'));
    self.assertFalse(codetags.isActive(['nil', 'tag-1']));
    self.assertFalse(codetags.isActive('nil', 'tag-3'));
    self.assertFalse(codetags.isActive('tag-3', 'disabled'));
    pass

  def test_isVersionValid(self):
    self.assertTrue(codetags._isVersionValid("0.1.4"))
    self.assertFalse(codetags._isVersionValid("0.a.b"))
    pass

  def test_isVersionLTE(self):
    self.assertFalse(codetags._isVersionLTE("0.1.4", "0.1.3"))
    self.assertTrue(codetags._isVersionLTE("0.1.4", "0.1.4"))
    self.assertTrue(codetags._isVersionLTE("0.1.4", "0.1.5"))
    self.assertTrue(codetags._isVersionLTE("0.1.4", "0.2.4"))
    with self.assertRaises(ValueError) as context:
      codetags._isVersionLTE("a.1.4", "0.2.4")
    with self.assertRaises(ValueError) as context:
      codetags._isVersionLTE("0.1.4", "z.2.4")
    pass

  def test_isVersionLT(self):
    self.assertFalse(codetags._isVersionLT("0.1.4", "0.1.3"))
    self.assertFalse(codetags._isVersionLT("0.1.4", "0.1.4"))
    self.assertTrue(codetags._isVersionLT("0.1.4", "0.1.5"))
    self.assertTrue(codetags._isVersionLT("0.1.4", "0.2.4"))
    with self.assertRaises(ValueError) as context:
      codetags._isVersionLT("a.1.4", "0.2.4")
    with self.assertRaises(ValueError) as context:
      codetags._isVersionLT("0.1.4", "z.2.4")
    pass

if __name__ == '__main__':
  unittest.main()
