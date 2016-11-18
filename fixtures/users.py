Lena = dict(uid=1, name='lena', password='123')
Peter = dict(uid=2, name='peter', password='123')
Adolf = dict(uid=3, name='adolf', password='123')

ulist = (Lena, Peter,Adolf)

def match(name, pwd):
  print name, pwd
  user = get_by_name(name)
  return user.get('password') == pwd if user else False

def get_by_name(name):
  users = [u for u in ulist if u.get('name') == name]
  return users[0] if len(users) else None
