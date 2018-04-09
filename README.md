# zagoload

zagoload is python package for downloading files.

[![Version](https://img.shields.io/pypi/v/zagoload.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/zagoload)
[![Python](https://img.shields.io/pypi/pyversions/zagoload.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/zagoload)
[![License](https://img.shields.io/pypi/l/zagoload.svg?maxAge=2592000?style=plastic)](ttps://pypi.python.org/pypi/zagoload)
[![Build Status](http://img.shields.io/travis/napuzba/zagoload.svg)](https://travis-ci.org/napuzba/zagoload)
 
zagoload supposts:
 - Remote files can be accessible thought HTTP and FTP protocols.
 - The files can be cached locally.

Usage sample:

```python
import zagoload

ff = zagoload.load(source)
if ff.valid:
  # if valid, process ff.target is the downloaded file in the file on disk
  print(ff.target)
  # or process ff.text - the content of the file
  print(ff.text)
``` 
See more samples at [Download Files with zagoload](https://napuzba.com/a/download-files-with-zagoload/).
