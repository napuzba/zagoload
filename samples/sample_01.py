
import zagoload

def download(source):
  def info(ss):
    import sys ;sys.stdout.write(ss + u'\n')

  ff = zagoload.load(source)

  if ff.valid:
    # if valid, process ff.target - the file on disk
    info( 'Download {0} => {1}'.format(ff.source,ff.target) )
    # or process ff.text - the content of the file
    info( u'{0} characters : {1}'.format(len(ff.text),ff.text[:15].__repr__() ) )
  else:
    info('Failed to download {0}'.format(ff.source))



download(u'http://www.google.com' )
download(u'ftp://ftp.funet.fi/pub/standards/RFC/rfc959.txt')
