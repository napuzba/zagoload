import zagoload
def download(source,target):
  def info(ss):
    import sys ;sys.stdout.write(ss + u'\n')
  ff = zagoload.load(source,target=target)
  if ff.valid:
    info(u'{0} => {1}'.format(ff.source,ff.target))
  else:
    info('Failed to download {0}'.format(ff.source))
download( 'http://www.google.com', '01.txt' )
download( 'http://www.google.com', '01' )
download( 'http://www.google.com', '@01.txt' )
