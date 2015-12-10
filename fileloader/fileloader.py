# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

import ftplib
import os
import os.path
import time
import socket
import codecs
import urllib
import urllib2
import hashlib
import base64


class Cache:
    """
    How should files be cached ?
    """

    """
    Download the source file to cache even if it exist in the cache.
    """
    Disabled = 0

    """
    Check in cache for the source file. if it does not exist download it.
    """
    Enabled  = 1

    """
    Check in cache for the source file. if it does not exist report that failure.
    """
    InCache  = 2

class FileRequest:
    """
    Request for downloading file
    """
    def __init__(self, source, target='', timeout=0, proxy=Cache.Enabled, contentType= '', retries=0, onDownloading = None, params = {} , autoLoad = True, maxCache=0 ):
        """
        Create a new FileRequest

        :param str source:
            Path of the source
        :param str target:
            Path of the downloaded file
        :param int timeout:
            Timeout in seconds
        :param Cache proxy:
            The cache strategy
        :param str contentType:
            Expected content type
        :param int retries:
            Number of retries
        :param callback onDownloading:
            Callback function to be called while downloading
        :param dict params:
            Get parameters
        :param bool autoLoad:
            Whether to load data
        :param int maxCache:
            Maximum cache time in seconds
        """
        self.source        = source
        self.base          = source
        self.target        = target
        self.timeout       = timeout
        self.proxy         = proxy
        self.contentType   = contentType
        self.retries       = retries
        self.onDownloading = onDownloading
        self.params        = params
        self.autoLoad      = autoLoad
        self.maxCache      = maxCache
        self.state         = FileRequest.idNew

    def loadData(self):
        """
        Load the data stored in the target to memory
        """
        if self.state == FileRequest.idOk:
            try:
                with codecs.open(self.target,encoding='utf8',errors='ignore') as ff:
                    self.data = ff.read()
            except Exception,ee:
                pass

    def clear(self):
        """
        Clear the current request
        """
        self.source = FileLoader.buildUrl(self.source,self.params)
        self.state  = FileRequest.idNew
        self.data   = ''

    @property
    def valid(self):
        """
        Whether the request was done successfully
        """
        return self.state == FileRequest.idOk

    @property
    def failed(self):
        """
        Whether the request was failed
        """
        return self.state != FileRequest.idOk
    """
    Request ran successfully
    """
    idOk   =  0
    """
    The request failed
    """
    idFail = -1
    """
    The run request
    """
    idNew  = -2

class FileLoader:
    """
    FileLoader allows to access in local files and remote files -- files which are accessible thought
    HTTP and FTP protocols -- in uniform way. The files can be cached locally.
    """
    def __init__(self,dirCache=None):
        """
        Create a new FileLoader

        :param str dirCache:
            The cache directory
        """
        self.dirCache = FileLoader.dirCache if dirCache == None else dirCache
        self.cachePattern = [2]
        FileLoader.ensureFoler(self.dirCache)

    def load(self, source, target='', timeout=0, proxy=Cache.Enabled, contentType= '', retries=0, onDownloading = None, params = {} , autoLoad = True, maxCache=0):
        """
        load a new request

        :param str source:
            Path of the source
        :param str target:
            Path of the downloaded file
        :param int timeout:
            Timeout in seconds
        :param Cache proxy:
            The cache strategy
        :param str contentType:
            Expected content type
        :param int retries:
            Number of retries
        :param callback onDownloading:
            Callback function to be called while downloading
        :param dict params:
            Get parameters
        :param bool autoLoad:
            Whether to load data
        :param int maxCache:
            Maximum cache time in seconds
        """
        req = FileRequest(source, target=target, timeout=timeout, proxy=proxy, contentType=contentType, retries=retries, onDownloading = onDownloading, params = params, autoLoad = autoLoad, maxCache=maxCache)
        self.request(req)
        return req

    def request(self, req):
        """
        Downloads a file located on req.source

        :param DownloadRequest req:
            The download request
        """
        req.clear()
        if   req.source.startswith('http') or req.source.startswith('ftp' ):
            self.loadRemote(req)
        elif req.source != '':
            self.loadLocals(req)

    def loadRemote(self, req ):
        """
        Downloads a file located on req.source

        :param DownloadRequest req:
            The download request
        """
        req.target = self.findCachedName(req.source , req.target, True)
        inCache = False
        if os.path.exists(req.target):
            cacheTime = time.time() - os.path.getmtime(req.target)
            if req.maxCache != 0 and cacheTime >= req.maxCache :
                os.remove(req.target)
            else:
                inCache = True
        if (req.proxy == Cache.InCache or req.proxy == Cache.Enabled) and inCache:
            self.log(u'Find Cache: <{1}> as <{0}>',req.source,req.target)
            req.state  = FileRequest.idOk
            req.target = req.target
        elif req.proxy == Cache.InCache and inCache == False:
            self.log(u'Miss Cache: <{1}> as <{0}>',req.source,req.target)
            req.state  = FileRequest.idFail
            return
        elif     req.source.startswith('http'):
            self.loadHTTP(req)
        elif req.source.startswith('ftp' ):
            self.loadFTP(req)
        if req.autoLoad:
            req.loadData()

    def loadHTTP(self,req):
        """
        Downloads a file located on req.source

        :param DownloadRequest req:
            The download request
        """
        self.setTimout(req.timeout)
        counter = 0
        if isinstance(req.source,unicode):
            req.source = req.source.encode('utf8')

        while (counter <= req.retries) and (req.state != FileRequest.idOk):
            if counter >= 1:
                self.log(u"Retry {0} : {1}",counter, req.source)
                time.sleep(1)
            counter += 1
            try:
                headers = { 'User-Agent' : 'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)' }
                ff = urllib2.urlopen( urllib2.Request(req.source, None, headers) )
                headers = ff.info()
                if req.contentType != '' and headers['Content-Type'].find(req.contentType)    == -1:
                    self.setTimout(req.timeout)
                    req.state = FileRequest.idFail
                    break
                if ff.code != 200 and ff.code >= 400:
                    continue
                with open(req.target, "wb") as fl:
                    if ff.headers.has_key('Content-Length') == False:
                        data = ff.read()
                        fl.write( data )
                    else:
                        fileSize = int(ff.headers['Content-Length'])
                        saveData = False
                        if (fileSize > 0):
                            lastTime = time.time()
                            downSize = lastSize = downSpeed = 0
                            while (downSize < fileSize):
                                chunk = 100 * 1024
                                if (downSize + chunk) > fileSize:
                                    chunk = fileSize - downSize
                                data = ff.read(chunk)
                                fl.write(data)
                                if saveData:
                                    self.data += data
                                downSize += chunk
                                if req.onDownloading:
                                    percent = 100 * downSize / fileSize
                                    deltaTime = time.time() - lastTime
                                    if deltaTime >= 1:
                                        downSpeed = (downSize - lastSize) / deltaTime
                                        lastTime, lastSize = time.time() , downSize
                                        req.onDownloading(fileSize,downSize, downSpeed)
                ff.close()
                req.target = req.target
                req.state = FileRequest.idOk
            except IOError, ee:
                if hasattr(ee, 'reason'):
                    self.log(u'Fail download <{0}>. Reason: {1}',req.source, str(ee.reason))
                elif hasattr(ee, 'code'):
                    self.log(u'Fail download <{0}>. The server could not fulfill the request. Error code: {1}',req.source,str(ee.code))
                req.state = FileRequest.idFail
            except Exception, ee:
                self.log(u'Fail download <{0}>',req.source)
                req.state = FileRequest.idFail
                self.logException(ee)
        if req.state != FileRequest.idOk and os.path.exists(req.target):
            os.remove(req.target)
        self.setTimout()

    def loadFTP(self, req):
        """
        Downloads a file located on source
        """
        req.state = FileRequest.idFail
        urlParser = UrlFtpParser(req.source)
        try:
            self.ftp = ftplib.FTP()
            self.ftp.connect(urlParser.host,urlParser.port)
            self.log(u'**** Connected to host "{0}"',urlParser.host)
        except (socket.error, socket.gaierror), e:
            self.log(u'ERR: cannot reach "{0}"',urlParser.host)
            return
        try:
            if urlParser.username != '':
                self.ftp.login(urlParser.username, urlParser.password)
                self.log(u'**** Logged in as {0}', urlParser.username)
            else:
                self.ftp.login()
                self.log(u'**** Logged in as "anonymous"')
        except ftplib.error_perm:
            self.log(u'ERR: cannot login')
            self.ftp.quit()
            return
        try:
            self.ftp.cwd(urlParser.path)
            self.log(u'**** Changed to "{0}" folder',urlParser.path)
        except ftplib.error_perm:
            self.log(u'ERR: cannot CD to "{0}"',urlParser.path)
            self.ftp.quit()
            return
        self.bytes = 0
        try:
            self.ftp.retrbinary('RETR {0}'.format(file), open(req.target, 'wb').write)
            self.target = req.target
            self.size = self.ftp.size(self.target)
            self.size_MB = float(self.size) / (1024 * 1024)
            self.log(u'**** Downloaded "{0}" to CWD'.file)
            self.ftp.quit()
            req.state = FileRequest.idOk
        except ftplib.error_perm:
            self.log(u'ERR: cannot read file "{0}"',file)
            os.unlink(self.file)
            self.ftp.quit()
            return

    def loadLocals(self, req):
        """
        Downloads a file located on source
        """
        if os.path.exists(req.source) == False:
            return
        req.state  = FileRequest.idOk
        req.target = req.source
        if req.autoLoad:
            req.loadData()

    def findCachedName(self, source, target, isCached):
        """
        Find the cached name of the file

        :param source:
            source file url
        :param target:
            target file path
        :param isCached:
            whether the the target is cached

        :return :str:
             the cached name of the file
        """
        sum = self.hash(source,16) if isCached else '0000000000000000'

        dirCache = self.dirCache
        kk = 0
        for aa in self.cachePattern:
            dirCache = os.path.join(dirCache, sum[kk:kk+aa])
            kk += aa
        FileLoader.ensureFoler(dirCache)
        if target == '':
            return os.path.join( dirCache , 'file_{0}.bin'.format(sum) )
        if target.startswith('@'):
            return target[1:]
        extIndex = target.rfind('.')
        if extIndex != -1:
            return os.path.join( dirCache , u'{0}_{1}{2}'.format(target[:extIndex],sum,target[extIndex:]) )
        return os.path.join( dirCache , '{0}_{1}{2}'.format(target, sum,'.bin') )

    def hash(self, ss, size = 6):
        """
        Hash ss

        :param str ss:
            String to hash
        :param int size:
            Hash size in characters

        :return :str:
            The hash value
        """
        if isinstance(ss,unicode):
            ss = ss.encode('utf8')
        hh = base64.urlsafe_b64encode(hashlib.sha224(ss).digest())
        return hh[:size]

    def setTimout(self,timeout = 60):
        """
        Set the timeout to network operations

        :param int timeout:
            The timeout in seconds
        """
        if timeout != 0:
            socket.setdefaulttimeout(timeout)

    def log(self,msg,*args):
        """
        Log message

        :param str msg:
            message to log
        """
        pass # sys.stdout.write(u'{0} : {1}\n'.format( "FileLoader" , msg ))


    def logException(self,ee):
        """
        Log exception

        :param Exception ee:
            exception
        """
        pass # sys.stdout.write(u'{0}\n'.format(str(ee)))

    loader = None
    dirCache = "Cache"
    @staticmethod
    def loads(source, target='', timeout=0, proxy=Cache.Enabled, contentType= '', retries=0, onDownloading = None, params = {} , autoLoad = True, maxCache=0):
        """
        load a new request

        :param str source:
            Path of the source
        :param str target:
            Path of the downloaded file
        :param int timeout:
            Timeout in seconds
        :param Cache proxy:
            The cache strategy
        :param str contentType:
            Expected content type
        :param int retries:
            Number of retries
        :param callcack onDownloading:
            Callback function to be called while downloading
        :param dict params:
            Get parameters
        :param bool autoLoad:
            Whetehr to load data
        :param int maxCache:
            Maximum cache time in seconds
        """
        if FileLoader.loader == None:
            FileLoader.loader = FileLoader()
        req = FileRequest(source, target=target, timeout=timeout, proxy=proxy, contentType=contentType, retries=retries, onDownloading = onDownloading, params = params, autoLoad = autoLoad, maxCache=maxCache)
        FileLoader.loader.request(req)
        return req

    @staticmethod
    def buildUrl(url, params):
        """
        Build a url with parameters

        :param str url:
            Base url
        :param dict params:
            Dictionary of key/value pairs

        :return :str:
            The built url
        """
        def urlencode_unicode(params):
            """
            Build a query string

            :param dict params:
                Dictionary of key/value pairs

            :return :str:
                The built query string
            """
            query = ''
            for s1,s2 in params.iteritems():
                if s2 == None:
                    continue
                if not isinstance(s1,unicode):
                    s1 = str(s1).decode('utf8')
                if not isinstance(s2,unicode):
                    s2 = str(s2).decode('utf8')
                if ( query != '' ):
                    query += '&';
                query += urllib.quote_plus(s1.encode('utf8'))
                query += '=';
                query += urllib.quote_plus(s2.encode('utf8'))
            return query
        if isinstance(url,unicode):
            url = url.encode('utf8')
        query = urlencode_unicode(params)
        joiner= ''
        if query != '':
            joiner = '?' if url.find('?') == -1 else '&'
        return "{0}{1}{2}".format(url,joiner,query)

    @staticmethod
    def ensureFoler(folder):
        """
        Create <folder> if does not exist yet

        :param str folder:
            The folder

        :return :bool:
            True if the folder exist or was created successfully
        """
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                return False
        return True