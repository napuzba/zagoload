import zagoload
import os
import time
def download(source,cacheMode, cacheTime=0):
  def info(ss):
    import sys ;sys.stdout.write(ss + u'\n')
  ff = zagoload.load(source,cacheMode=cacheMode,cacheTime=cacheTime)
  if ff.valid:
    info( u'{0} => {1}. Time : {2:.2f}'.format(ff.source, ff.target, os.path.getmtime(ff.target) % 10000) )
  else:
    info( 'Failed to download {0}'.format(ff.source) )
# will fail since no file in cache
download( 'http://www.google.com', zagoload.CacheMode.InCache     )

# will download from source
download( 'http://www.google.com', zagoload.CacheMode.Enabled     )

# will use cached file
download( 'http://www.google.com', zagoload.CacheMode.Enabled     )

# will use cached file
download( 'http://www.google.com', zagoload.CacheMode.InCache     )

# will download the file from source, even though the file exist in cache
download( 'http://www.google.com', zagoload.CacheMode.Disabled    )

# will use cached file
download( 'http://www.google.com', zagoload.CacheMode.Enabled     )

# will download the file from source, since the cached file is older than 5 seconds
time.sleep(10)
download( 'http://www.google.com', zagoload.CacheMode.Enabled  , 5)
