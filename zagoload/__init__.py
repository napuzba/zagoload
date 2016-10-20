# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]


from .cachemode   import CacheMode
from .filerequest import FileRequest
from .ftpinfo     import FtpInfo
from .fileloader  import FileLoader

loader = FileLoader("Cache")

def load(
        source            ,
        target      = ''  ,
        params      = {}  ,
        postdata    = {}  ,
        timeout     = 0   ,
        retries     = 0   ,
        contentType = ''  ,
        onDownload  = None,
        autoText    = True,
        autoJson    = False,
        cacheMode   = CacheMode.Enabled ,
        cacheTime   = 0    ,
        action      = 'GET',
        headers     = {}   ):

    '''
    '''
    req = FileRequest(
        source                   ,
        target      = target     ,
        params      = params     ,
        postdata    = postdata   ,
        timeout     = timeout    ,
        retries     = retries    ,
        contentType = contentType,
        onDownload  = onDownload ,
        autoText    = autoText   ,
        autoJson    = autoJson   ,
        cacheMode   = cacheMode  ,
        cacheTime   = cacheTime  ,
        headers     = headers    )
    return loader.request(req)

def json(
        source            ,
        target      = ''  ,
        params      = {}  ,
        postdata    = {}  ,
        timeout     = 0   ,
        retries     = 0   ,
        contentType = ''  ,
        onDownload  = None,
        autoText    = False,
        autoJson    = True,
        cacheMode   = CacheMode.Enabled ,
        cacheTime   = 0    ,
        action      = 'GET',
        headers     = {}   ):
    '''
    '''
    req = FileRequest(
        source                   ,
        target      = target     ,
        params      = params     ,
        postdata    = postdata   ,
        timeout     = timeout    ,
        retries     = retries    ,
        contentType = contentType,
        onDownload  = onDownload ,
        autoText    = autoText   ,
        autoJson    = autoJson   ,
        cacheMode   = cacheMode  ,
        cacheTime   = cacheTime  ,
        headers     = headers    )
    return loader.request(req)
