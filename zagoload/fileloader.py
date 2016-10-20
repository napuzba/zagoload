# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

import base64
import codecs
import ftplib
import hashlib
import io
import time
import urllib3
import socket
import os
import os.path
import sys

from .cachemode   import CacheMode
from .filerequest import FileRequest, RequestState
from .ftpinfo     import FtpInfo
from .            import helpers

class FileLoader:
    '''
    FileLoader allows to access in local files and remote files -- files which are accessible thought
    HTTP and FTP protocols -- in uniform way. The files can be cached locally.
    '''
    def __init__(self,dirCache="cache"):
        '''
        Create a new FileLoader

        :param str dirCache:
            The cache directory
        '''
        self.dirCache = dirCache
        self.cachePattern = [2]
        urllib3.disable_warnings()
        self.http = urllib3.PoolManager()

        helpers.ensureFoler(self.dirCache)

    def load(self,
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
        headers     = {}  ):
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
            headers     = headers
        )
        return self.request(req)

    def request(self, req):
        '''
        Downloads a file located on req.source

        :param DownloadRequest req:
            The download request
        '''
        req.clear()
        if   req.source.startswith('http'):
            self.loadHttp (req)
        elif req.source.startswith('ftp' ):
            self.loadFtp  (req)
        elif req.source != ''             :
            self.loadLocal(req)

        if req.valid and req.autoText:
            req.loadText()
        if req.valid and req.autoJson:
            req.loadJson()
        return req

    def checkCache(self,req):
        '''
        Check whether the file in cache

        :param FileRequest req:
            The download request
        '''
        req.target = self.findCachedName(req.source , req.target, True)
        req.state  = RequestState.PendingCache
        inCache = False
        if os.path.exists(req.target):
            cacheTime = time.time() - os.path.getmtime(req.target)
            if req.cacheTime != 0 and cacheTime >= req.cacheTime :
                os.remove(req.target)
            else:
                inCache = True
        if (req.cacheMode == CacheMode.InCache or req.cacheMode == CacheMode.Enabled) and inCache:
            self.log(u'Find Cache: <{1}> as <{0}>',req.source,req.target)
            req.state  = RequestState.Cached
            req.target = req.target
            return
        if req.cacheMode == CacheMode.InCache and inCache == False:
            self.log(u'Miss Cache: <{1}> as <{0}>',req.source,req.target)
            req.state  = RequestState.FailMissCache
            return
        req.state  = RequestState.PendingDownload

    def loadHttp(self,req):
        '''
        Downloads a file located on req.source

        :param DownloadRequest req:
            The download request
        '''
        self.checkCache(req)
        if req.state  != RequestState.PendingDownload:
            return
        counter = 0
        if sys.version_info[0] == 2:
            if isinstance(req.source,str):
                req.source = req.source.encode('utf8')
        while (counter <= req.retries) and (req.state != RequestState.Downloaded):
            if counter >= 1:
                self.log(u"Retry {0} : {1}",counter, req.source)
                time.sleep(1)
            counter += 1
            try:
                ff = None
                if not req.postdata:
                    ff = self.http.urlopen(req.action , req.source ,preload_content=False )
                else:
                    ff = self.http.request(req.action , req.source ,preload_content=False , fields = req.postdata )
                req.rHeaders = ff.headers
                req.rStatus  = ff.status
                if ff.status != 200 and ff.status >= 400:
                    continue
                if req.contentType != '' and ff.headers['Content-Type'].find(req.contentType) == -1:
                    req.state = RequestState.FailDownload
                    break
                fileSize = None
                if 'Content-Length' in ff.headers:
                    fileSize = int(ff.headers['Content-Length'])
                chunkSize = 4*1024
                bb = io.BufferedReader(ff, chunkSize)
                with open(req.target, "wb") as fl:
                    lastTime = time.time()
                    downSize = lastSize = downSpeed = 0
                    while True:
                        data = bb.read(chunkSize)
                        dataSize = len(data)
                        fl.write(data)
                        downSize += dataSize
                        if req.onDownload != None:
                            deltaTime = time.time() - lastTime
                            if deltaTime >= 1:
                                downSpeed = (downSize - lastSize) / deltaTime
                                lastTime, lastSize = time.time() , downSize
                                req.onDownload(fileSize,downSize, downSpeed)
                        if downSize == fileSize or dataSize < chunkSize or dataSize == 0:
                            break
                req.target = req.target
                req.state  = RequestState.Downloaded
            except IOError as ee:
                req.state = RequestState.FailDownload
                if hasattr(ee, 'reason'):
                    self.log(u'Fail download <{0}>. Reason: {1}',req.source, str(ee.reason))
                elif hasattr(ee, 'code'):
                    self.log(u'Fail download <{0}>. The server could not fulfill the request. Error code: {1}',req.source,str(ee.code))
            except Exception as ee:
                req.state = RequestState.FailDownload
                self.log(u'Fail download <{0}>',req.source)
                self.logException(ee)
        if req.failed and os.path.exists(req.target):
            os.remove(req.target)

    def loadFtp(self, req):
        '''
        Downloads a file located on source
        '''
        self.checkCache(req)
        if req.state  != RequestState.PendingDownload:
            return

        ftpInfo = FtpInfo().parse(req.source)
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(ftpInfo.host,ftpInfo.port)
            self.log(u'**** Connected to host "{0}"',ftpInfo.host)
        except (socket.error, socket.gaierror) as e:
            self.log(u'ERR: cannot reach "{0}"',ftpInfo.host)
            req.state = filerequest.RequestState.FailDownload
            return
        try:
            if ftpInfo.username != '':
                self.ftp.login(ftpInfo.username, ftpInfo.password)
                self.log(u'**** Logged in as {0}', ftpInfo.username)
            else:
                self.ftp.login()
                self.log(u'**** Logged in as "anonymous"')
        except ftplib.error_perm:
            self.log(u'ERR: cannot login')
            req.state = filerequest.RequestState.FailDownload
            self.ftp.quit()
            return
        try:
            self.ftp.cwd(ftpInfo.path)
            self.log(u'**** Changed to "{0}" folder',ftpInfo.path)
        except ftplib.error_perm:
            self.log(u'ERR: cannot CD to "{0}"',ftpInfo.path)
            req.state = filerequest.RequestState.FailDownload
            self.ftp.quit()
            return
        self.bytes = 0
        try:
            self.ftp.retrbinary('RETR {0}'.format(ftpInfo.file), open(req.target, 'wb').write)
            self.target = req.target
            self.log(u'**** Downloaded "{0}" to CWD',ftpInfo.file, self.target)
            self.ftp.quit()
            req.state = RequestState.Downloaded
        except ftplib.error_perm:
            self.log(u'ERR: cannot read file "{0}"',file)
            os.unlink(self.file)
            req.state = RequestState.FailDownload
            self.ftp.quit()
            return

    def loadLocal(self, req):
        '''
        Downloads a file located on source
        '''
        if os.path.exists(req.source) == False:
            req.state = RequestState.FailDownload
            return
        req.state  = RequestState.Downloaded
        req.target = req.source

    def findCachedName(self, source, target, isCached):
        '''
        Find the cached name of the file

        :param source:
            source file url
        :param target:
            target file path
        :param isCached:
            whether the the target is cached

        :return :str:
             the cached name of the file
        '''
        if target.startswith('@'):
            return target[1:]

        sum = self.hash(source,16) if isCached else '0000000000000000'
        dirCache = self.dirCache
        kk = 0
        for aa in self.cachePattern:
            dirCache = os.path.join(dirCache, sum[kk:kk+aa])
            kk += aa
        helpers.ensureFoler(dirCache)
        if target == '':
            return os.path.join( dirCache , 'file_{0}.bin'.format(sum) )
        extIndex = target.rfind('.')
        if extIndex != -1:
            return os.path.join( dirCache , u'{0}_{1}{2}'.format(target[:extIndex],sum,target[extIndex:]) )
        return os.path.join( dirCache , '{0}_{1}{2}'.format(target, sum,'.bin') )

    def hash(self, ss, size = 6):
        '''
        Hash ss

        :param str ss:
            String to hash
        :param int size:
            Hash size in characters

        :return :str:
            The hash value
        '''
        if sys.version_info[0] >= 3 or isinstance(ss,unicode):
            ss = ss.encode('utf8')
        hh = base64.urlsafe_b64encode(hashlib.sha224(ss).digest())
        if sys.version_info[0] == 3:
            hh = hh.decode('ascii')

        return hh[:size]

    def log(self,msg,*args):
        '''
        Log message

        :param str msg:
            message to log
        '''
        pass # sys.stdout.write(u'{0} : {1}\n'.format( "FileLoader" , msg.format(*args) ))

    def logException(self,ee):
        '''
        Log exception

        :param Exception ee:
            exception
        '''
        pass # sys.stdout.write(u'{0} : {1}\n'.format( "FileLoader" , str(ee) ))
