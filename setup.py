# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

from distutils.core import setup

description = 'Downloading files (http,ftp).Supports: cachinhg, uniform access to remote and local files'
long_description = '''
=====
About
=====

fileloader module simplifies downloading and accessing remote files. 

********
Features
********

1. Allows uniform access to Remote files ( accessible thought HTTP and FTP protocols) and local files.
2. Support caching

*****
Usage
*****

See `Download Files with Fileloader`_ for turorial.

.. _Download Files with Fileloader: http://www.napuzba.com/story/download-files-with-fileloader/
'''

setup(
  name             = 'fileloader',
  packages         = ['fileloader'], 
  install_requires=[
     'urllib3 >= 1.0',
  ],
  version          = '2.0.2',  
  author           = 'napuzba',
  author_email     = 'kobi@napuzba.com',
  url              = 'https://github.com/napuzba/fileloader.git',
  download_url     = 'https://github.com/napuzba/fileloader/releases',
  description      = description,
  long_description = long_description,
  keywords         = ['download,crawl,ftp,http'],
  classifiers      = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: File Transfer Protocol (FTP)',    
    'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
  ],
)