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

if __name__ == '__main__':
  unittest.main()
