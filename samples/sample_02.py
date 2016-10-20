import re
import zagoload

def queryBing(query,count):
  def info(ss):
    import sys ;sys.stdout.write(ss + u'\n')
  def cleanTags(text):
    return re.sub(u'<(.*?)>','',text)
  # download url
  params = {}
  params['q'] = query
  ff = zagoload.load('http://www.bing.com/',params=params)
  if ff.valid:
    info(u'{0} => {1}'.format(ff.source,ff.target))
    info(u'Bing <{1}> - Top {0}'.format(count,query))
    reCite = '<cite>(?P<link>.*?)</cite>'
    zz = 0
    for ii in re.finditer( reCite , ff.text , re.DOTALL ):
      link = cleanTags(ii.group('link'))
      zz += 1
      info(u'  {0} => {1}'.format(zz,link))
      if zz == count:
        break
  else:
    info(u'Failed to download {0}'.format(ff.source))

queryBing( 'python', 3 )
queryBing( 'php'   , 3 )
