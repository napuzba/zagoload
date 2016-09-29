# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

import os
import sys

def buildUrl(url, params):
    '''
    Build a url with parameters

    :param str url:
        Base url
    :param dict params:
        Dictionary of key/value pairs

    :return :str:
        The built url
    '''
    def urlencode_unicode(params):
        '''
        Build a query string

        :param dict params:
            Dictionary of key/value pairs

        :return :str:
            The built query string
        '''
        query = ''
        for s1,s2 in params.items():
            if s2 == None:
                continue
            if ( query != '' ):
                query += '&';
            if sys.version_info[0] == 2:
                if not isinstance(s1,unicode): s1 = str(s1).decode('utf8')
                if not isinstance(s2,unicode): s2 = str(s2).decode('utf8')
                s1 = s1.encode('utf8')
                s2 = s2.encode('utf8')
                import urllib
                query += urllib.quote_plus(s1) + '=' + urllib.quote_plus(s2)
            if sys.version_info[0] >= 3:
                if not isinstance(s1,str): s1 = str(s1)
                if not isinstance(s2,str): s2 = str(s2)
                import urllib.parse
                query += urllib.parse.quote_plus(s1) + '=' + urllib.parse.quote_plus(s2)
        return query
    if sys.version_info[0] == 2:
        if isinstance(url,str):
            url = url.encode('utf8')
    query = urlencode_unicode(params)
    joiner= ''
    if query != '':
        joiner = '?' if url.find('?') == -1 else '&'
    return u"{0}{1}{2}".format(url,joiner,query)

def ensureFoler(folder):
    '''
    Create <folder> if does not exist yet

    :param str folder:
        The folder

    :return :bool:
        True if the folder exist or was created successfully
    '''
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            return False
    return True
