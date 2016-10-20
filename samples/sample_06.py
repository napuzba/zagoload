import zagoload

def find_post_title(id):
 ff = zagoload.json( 'https://jsonplaceholder.typicode.com/posts/{0}'.format(id) )
 return ff.json['title']

def find_users():
  ff = zagoload.json( 'https://jsonplaceholder.typicode.com/users' )
  return [user['username'] for user in ff.json]

def add_post(postdata = {}):
  ff = zagoload.json('http://jsonplaceholder.typicode.com/posts', action='POST', postdata = postdata , cacheMode=zagoload.CacheMode.Disabled )
  return ff.rStatus == 200

def run():
  print( find_post_title(1)  )
  print( find_users() )
  if add_post({ 'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1 }):
    print("Added")

run()
