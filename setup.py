#!/usr/bin/env python

from distutils.core import setup

setup(name='pyanxdns',
      version='0.1',
      license='MIT'
      description='Python client to communicate with ANX DNS API',
      author='Marky Egebäck',
      author_email='marky@egeback.se',
      url='https://github.com/egeback/pyanxdns',
      packages=['pyanxdns'],
      install_requires=[],
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