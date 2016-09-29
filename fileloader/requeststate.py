# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

class RequestState:
    '''
    The state of the request
    '''

    '''
    The file was downloaded succesfully
    '''
    Downloaded        =  1
    '''
    The file was read from cache
    '''
    Cached            =  2
    '''
    The file was not downloaded successfully
    '''
    FailDownload      = 11
    '''
    The file was not in cache
    '''
    FailMissCache     = 12
    '''
    The request is new
    '''
    PendingNew        = 21
    '''
    The request is check in cache for existence
    '''
    PendingCache      = 22
    '''
    The file should be downloaded
    '''
    PendingDownload   = 23
