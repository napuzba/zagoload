# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

class FtpInfo:
    '''
    Info of file accessible via ftp protocol ( username, password, host, port, path, file )
    '''
    def __init__(self, host='', path='',file='',port=21, username='', password=''):
        '''
        Create a new FtpInfo
        :param str host:
            The host of the ftp server
        :param str path:
            The path where the file is located
        :param str file:
            The name of the file
        :param int port:
            The port of the ftp server
        :param str username:
            The username used to login to the ftp server
        :param str password:
            The password used to login to the ftp server
        '''
        self.username = username
        self.password = password
        self.port     = port
        self.host     = host
        self.file     = file
        self.path     = path
        self.valid    = True

    def parse(self,url):
        '''
        Parse URL according RFC 1738: ftp://user:password@host:port/path/file

        param str url:
            The url to parse
        '''
        if url.startswith('ftp://') == False:
            self.valid = False
            return self
        x0 = len('ftp://')

        #check for username, password
        x1 = url.find('@',x0)
        if x1 != -1:
            x2 = url.find(':',x0,x1)
            if x2 != -1:
                self.username = url[x0  : x2]
                self.password = url[x2+1: x1]
            url = url[x1+1:]
        else:
            url = url[x0:]

        #check for host
        x3 = url.find('/')
        if x3 != -1:
            self.host = url[:x3]
            self.path = url[x3:]
        else:
            self.host = url
            self.path = ''

        #retrieve the port
        x4 = self.host.find(':')
        if x4 != -1:
            self.port = int(self.host[x4+1:])
            self.host = self.host[:x4]

        #split path and file
        x5 = self.path.rfind('/')
        if x5 != -1:
            self.file = self.path[x5+1:]
            self.path = self.path[:x5]
        else:
            self.file = ''
        return self

    def __str__(self):
        slogin = ''
        if self.username == '':
            slogin = self.username+':'+self.password + '@'
        if self.port != 21:
            sport  = ':' + str(self.port)
        return 'ftp://'+ slogin + self.host + self.path + '/' + self.file
