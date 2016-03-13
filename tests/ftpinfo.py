# Copyright (C) 2014 Napuzba [kobi@napuzba.com]
# Licensed under MIT license [http://openreq.source.org/licenses/MIT]

import unittest
import fileloader

class TestFtpInfo(unittest.TestCase):
    def test_parse(self):
        self.assertParse( 'ftp://host'                           , 'host' , ''       , ''     , 21  , '', '' )
        self.assertParse( 'ftp://host:2121'                      , 'host' , ''       , ''     , 2121, '', '' )
        self.assertParse( 'ftp://host/file'                      , 'host' , ''       , 'file' , 21  , '', '' )
        self.assertParse( 'ftp://host/p1/p2/file'                , 'host' , '/p1/p2' , 'file' , 21  , '', '' )
        self.assertParse( 'ftp://name:pass@host/p1/p2/file'      , 'host' , '/p1/p2' , 'file' , 21  , 'name', 'pass' )
        self.assertParse( 'ftp://name:pass@host:2121/p1/p2/file' , 'host' , '/p1/p2' , 'file' , 2121, 'name', 'pass' )
        self.assertParse( 'http://host.com'                      , ''     , ''       , ''     , 21  , ''    , ''     , False )

    def assertParse(self, url, host, path, file, port, username, password, valid = True):
        fi =  fileloader.FtpInfo().parse(url)
        self.assertEqual(fi.username , username)
        self.assertEqual(fi.password , password)
        self.assertEqual(fi.host     , host    )
        self.assertEqual(fi.port     , port    )
        self.assertEqual(fi.path     , path    )
        self.assertEqual(fi.file     , file    )

if __name__ == '__main__':
    unittest.main()
