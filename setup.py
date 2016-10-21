# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

from setuptools import setup

description = 'Download files(http,ftp). Supports: cachinhg, uniform access to remote and local files'
long_description = '''
=====
About
=====

zagoload module simplifies downloading and accessing remote files:

1. Access to Remote files (accessible thought HTTP and FTP protocols) and local files in uniform way.
2. Consume restful webservices with a breeze
3. Cache your downloaded files to save resources

*****
Usage
*****

See `Download Files with zagoload`_ for turorial.

.. _Download Files with Fileloader: http://www.napuzba.com/story/download-files-with-zagoload/
'''

setup(
  name             = 'zagoload',
  packages         = ['zagoload'],
  install_requires = [
     'urllib3 >= 1.0',
  ],
  version          = '0.5.0',
  author           = 'napuzba',
  author_email     = 'kobi@napuzba.com',
  url              = 'https://github.com/napuzba/zagoload.git',
  description      = description,
  long_description = long_description,
  license          = 'MIT',
  keywords         = ['download,crawl,ftp,http,json,webservices,cache'],
  classifiers      = [
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: File Transfer Protocol (FTP)',
    'Topic :: Internet :: WWW/HTTP :: Indexing/Search',

    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',

    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Intended Audience :: System Administrators',
  ],
)
