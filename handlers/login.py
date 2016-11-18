from bottle import *
from fixtures import users
import auth

@post('/login')
def do_login():
  username = request.json.get('username', '')
  password = request.json.get('password', '')
  if not users.match(username, password):
    response.status = 403
    return dict(ok=False, message=False)
  user = users.get_by_name(username)
  atk, rtk = auth.for_user(user.get('uid'), request.environ.get('HTTP_USER_AGENT'))
  return dict(ok=True, auth=dict(access_token=atk, refresh_token=rtk))

