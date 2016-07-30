#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Discogs Jockey',
      version='0.1',
      description='DJ mixing tool',
      url='https://github.com/AP-e/Discogs-Jockey',
      packages=['discogs_jockey']
     )

