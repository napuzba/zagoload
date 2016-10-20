# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

import codecs
import json

from . import helpers
from .requeststate import RequestState
from .cachemode    import CacheMode


class FileRequest:
    '''
    Request for downloading file
    '''
    def __init__(self,
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
        cacheTime   = 0   ,
        headers     = {}  ,
        action      = 'GET'):
        '''
        Create a new FileRequest
        :param str source:
            Path of the source
        :param str target:
            Path of the downloaded file
        :param dict params:
            Get parameters
        :param dict params:
            Post parameters
        :param int timeout:
            Timeout in seconds
        :param int retries:
            Number of retries
        :param str contentType:
            Expected content type
        :param callback onDownload:
            Callback function to be called while downloading
        :param bool loadText:
            Whether to load text
        :param int cacheTime:
            Maximum cache time in seconds
        :param Cache cachMode:
            The cache strategy
        :param dict headers:
            The headers of the request
        '''
        self.source      = source

        self.target      = target
        self.params      = params
        self.postdata    = postdata
        self.timeout     = timeout
        self.retries     = retries
        self.contentType = contentType
        self.onDownload  = onDownload
        self.autoText    = autoText
        self.autoJson    = autoJson
        self.state       = RequestState.PendingNew
        self.headers     = headers
        self.cacheTime   = cacheTime
        self.cacheMode   = cacheMode
        self.action      = action

        self.base        = source
        if ('User-Agent' in self.headers) == False:
            self.headers['User-Agent'] = 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)'

    def loadText(self):
        '''
        Load the text stored in the target to memory
        '''
        if self.valid == False:
            return
        try:
            with codecs.open(self.target,encoding='utf8',errors='ignore') as ff:
                self.text = ff.read()
        except Exception as ee:
            pass

    def loadJson(self):
        if self.valid == False:
            return
        try:
            with codecs.open(self.target,encoding='utf8',errors='ignore') as ff:
                self.json = json.load(ff)
        except:
            pass

    def clear(self):
        '''
        Clear the current request
        '''
        self.source   = helpers.buildUrl(self.base,self.params)
        self.state    = RequestState.PendingNew
        self.text     = ''
        self.json     = None
        self.rStatus  = 0
        self.rHeaders = {}

    @property
    def valid(self):
        '''
        Whether the request was done successfully
        '''
        return self.state == RequestState.Downloaded or self.state == RequestState.Cached

    @property
    def failed(self):
        '''
        Whether the request was failed
        '''
        return self.state == RequestState.FailDownload or self.state == RequestState.FailMissCache

    @property
    def pending(self):
        '''
        Whether the request is not completed
        '''
        return not ( self.valid and self.failed)
