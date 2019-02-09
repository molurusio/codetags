#!/usr/bin/env python

from setuptools import setup
import codetags as package

setup(
  name = package.__name__,
  version = package.__version__,
  description = package.__doc__.strip(),
  long_description = read_file('README.rst'),
  author = package.__author__,
  author_email = package.__author_email__,
  url = 'https://github.com/molurusio/codetags',
  download_url = 'https://github.com/molurusio/codetags/downloads',
  license = package.__license__,
  py_modules = [package.__name__],
  keywords = ['molurus', 'codetags', 'feature-toggle'],
  classifiers = [],
)