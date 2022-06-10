#!/usr/bin/env python

from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyanxdns',
      version='0.2.5',
      license='MIT',
      description='Python client to communicate with ANX DNS API',
      author='Marky Egebäck',
      author_email='marky@egeback.se',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/egeback/pyanxdns',
      packages=['pyanxdns'],
      install_requires=['requests'],
      classifiers=(
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Topic :: Utilities",
        )
     )
