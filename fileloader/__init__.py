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
        timeout     = 0   ,
        retries     = 0   ,
        contentType = ''  ,
        onDownload  = None,
        autoLoad    = True,
        cacheMode   = CacheMode.Enabled ,
        cacheTime   = 0   ,
        headers     = {}  ):
    '''
    '''
    req = FileRequest(
        source                   ,
        target      = target     ,
        params      = params     ,
        timeout     = timeout    ,
        retries     = retries    ,
        contentType = contentType,
        onDownload  = onDownload ,
        autoLoad    = autoLoad   ,
        cacheMode   = cacheMode  ,
        cacheTime   = cacheTime  ,
        headers     = headers    )
    return loader.request(req)


