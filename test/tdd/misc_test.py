#!/usr/bin/env python

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../codetags')

from misc import misc

class MiscTest(unittest.TestCase):

  def test_libelify(self):
    self.assertEqual(misc.labelify(None), None);
    self.assertEqual(misc.labelify(""), "");
    self.assertEqual(misc.labelify("Hello  world"), "HELLO_WORLD");
    self.assertEqual(misc.labelify("Underscore_with 123"), "UNDERSCORE_WITH_123");
    self.assertEqual(misc.labelify("user@example.com"), "USER_EXAMPLE_COM");
    pass

if __name__ == '__main__':
  unittest.main()
