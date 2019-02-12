#!/usr/bin/env python

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../codetags')

from main import default as codetags
from main import newInstance

class CodetagsTest(unittest.TestCase):

  def test_invalid_instance_name(self):
    # with self.assertRaises(Exception) as context:
    #   newInstance(1024)
    # self.assertTrue('This is broken' in context.exception)
    pass

  def test_always_true(self):
    codetags.initialize(**{
        'namespace': 'codetags',
        'positiveTagsLabel': 'INCLUDED_TAGS',
        'negativeTagsLabel': 'EXCLUDED_TAGS',
        'version': '0.1.7',
    })
    self.assertTrue(True)
    pass

if __name__ == '__main__':
  unittest.main()
