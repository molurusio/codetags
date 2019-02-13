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

  def test_stringToArray(self):
    self.assertListEqual(misc.stringToArray(None), [])
    self.assertListEqual(misc.stringToArray(""), [])
    self.assertListEqual(misc.stringToArray(123), [])
    self.assertListEqual(misc.stringToArray("abc"), ["abc"])
    self.assertListEqual(misc.stringToArray("abc , def"), ["abc", "def"])
    self.assertListEqual(misc.stringToArray("abc, ,def"), ["abc", "def"])
    pass
  
  def test_isVersionValid(self):
    self.assertTrue(misc.isVersionValid("0.1.4"))
    self.assertFalse(misc.isVersionValid("0.a.b"))
    pass

  def test_isVersionLTE(self):
    self.assertFalse(misc.isVersionLTE("0.1.4", "0.1.3"))
    self.assertTrue(misc.isVersionLTE("0.1.4", "0.1.4"))
    self.assertTrue(misc.isVersionLTE("0.1.4", "0.1.5"))
    self.assertTrue(misc.isVersionLTE("0.1.4", "0.2.4"))
    with self.assertRaises(ValueError) as context:
      misc.isVersionLTE("a.1.4", "0.2.4")
    with self.assertRaises(ValueError) as context:
      misc.isVersionLTE("0.1.4", "z.2.4")
    pass

  def test_isVersionLT(self):
    self.assertFalse(misc.isVersionLT("0.1.4", "0.1.3"))
    self.assertFalse(misc.isVersionLT("0.1.4", "0.1.4"))
    self.assertTrue(misc.isVersionLT("0.1.4", "0.1.5"))
    self.assertTrue(misc.isVersionLT("0.1.4", "0.2.4"))
    with self.assertRaises(ValueError) as context:
      misc.isVersionLT("a.1.4", "0.2.4")
    with self.assertRaises(ValueError) as context:
      misc.isVersionLT("0.1.4", "z.2.4")
    pass

if __name__ == '__main__':
  unittest.main()
