#!/usr/bin/env python

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../codetags')

from main import default as codetags

class CodetagsTest(unittest.TestCase):

  def test_always_true(self):
    codetags.initialize(**{
        'host': 'abc',
    })
    self.assertTrue(True)
    pass

if __name__ == '__main__':
  unittest.main()
