#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='build2l',
      version='0.1',
      description='Client tool / library for rebuilding packages',
      author='Honza Horak',
      author_email='hhorak@redhat.com',
      url='https://github.com/hhorak/build2l',
      entry_points={
          'console_scripts': ['build2l=build2l.generator:main'],
      },
      packages=find_packages(),
)
