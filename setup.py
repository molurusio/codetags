#!/usr/bin/env python

import setuptools
import codetags as package

setuptools.setup(
  name = package.__name__,
  version = package.__version__,
  description = package.__doc__.strip(),
  author = package.__author__,
  author_email = package.__author_email__,
  url = 'https://github.com/molurusio/codetags',
  download_url = 'https://github.com/molurusio/codetags/downloads',
  license = package.__license__,
  py_modules = [package.__name__],
  keywords = ['molurus', 'codetags', 'feature-toggle'],
  classifiers = [],
  packages = setuptools.find_packages(),
)