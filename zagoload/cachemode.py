# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

class CacheMode:
    '''
    How should files be cached ?
    '''

    '''
    Download the source file to cache even if it exist in the cache.
    '''
    Disabled = 0

    '''
    Check in cache for the source file. if it does not exist download it.
    '''
    Enabled  = 1

    '''
    Check in cache for the source file. if it does not exist report that failure.
    '''
    InCache  = 2
