# -*- coding: utf-8 -*-
import os
import io
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.rst'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.rst'), encoding='UTF-8').read()

setup(name="cid",
      version='0.1',
      description="Extract Chinese identity card info (gender, birthday \
          and regions)",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='chinese-identity',
      author="Eric Lo",
      author_email="lxneng@gmail.com",
      url="https://github.com/lxneng/cid",
      packages=find_packages('src'),
      test_suite='cid.tests',
      package_dir={'': 'src'},
      include_package_data=True,
      license="BSD")
