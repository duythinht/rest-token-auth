from bottle import *
import auth
import time

@post('/auth/access_token')
def request_access_token():
  """
  In order of darkness we deciced to implements by POST method to secure more than query string
  """
  refresh_token = request.json.get('refresh_token', 'None')
  try:
    access_token = auth.request_atk_by_rf(refresh_token)
    return dict(ok=True, access_token=access_token)
  except auth.InvalidToken:
    return auth.e401('Invalid token')
  except auth.Expired:
    return auth.e401('Token has been expired')

@post('/auth/refresh_token/extend')
def request_access_token():
  """
  In order of darkness we deciced to implements by POST method to secure more than query string
  """
  refresh_token = request.json.get('refresh_token', 'None')
  try:
    refresh_token = auth.extend(refresh_token)
    return dict(ok=True, refresh_token=refresh_token)
  except auth.InvalidToken:
    return auth.e401('Invalid token')
  except auth.Expired:
    return auth.e401('Token has been expired')

@get('/auth/sessions')
@auth.login_required
def auth_session_list():
  uid = request.uid
  return dict(ok=True, sessions=[s for s in auth.sessions_of(uid)])
