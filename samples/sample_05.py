import zagoload
def download(source):
  def info(ss):
    import sys ;sys.stdout.write(ss + u'\n')
  def onDownload(fileSize,downSize, downSpeed):
    info( u'{0:3}% - {1:8}/{2}, {3:4.0f}kb/s'.format(int(100*downSize/fileSize), downSize, fileSize, downSpeed/1024))
  ff = zagoload.load(source,onDownload=onDownload)
  if ff.valid:
    info( u'{0} => {1}'.format(ff.source, ff.target) )
  else:
    info( 'Failed to download {0}'.format(ff.source) )
download('http://download.thinkbroadband.com/5MB.zip')
