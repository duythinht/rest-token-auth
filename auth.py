import jwt, uuid
from connection import redis
import time
from functools import wraps
from bottle import response, request

SSAGENT_KEY = 'auth:ssid:%s:agent'
USSL_KEY = 'auth:uid:%s:SSL' # user ss list
SECRET = 'khongbiet'

def for_user(uid, agent):
  ssid = new_ssid(uid, agent) 
  return make_access_token(uid, ssid), make_refresh_token(uid, ssid)

def new_ssid(uid, agent):
  ssid = uuid.uuid4().hex
  redis.rpush(USSL_KEY % uid, ssid)
  redis.setex(SSAGENT_KEY % ssid, 86400 * 60, agent) # expire for 2 month
  return ssid

def make_access_token(uid, ssid):
  payload = dict(uid=uid, ssid=ssid, exp=exp_time_for(15))
  return jwt.encode(payload, SECRET)

def make_refresh_token(uid, ssid):
  payload = dict(uid=uid, ssid=ssid, exp=exp_time_for(86400))
  return jwt.encode(payload, SECRET)

def exp_time_for(_minutes):
  return int(time.time()) + _minutes * 60

def decode_and_check(token):
  try:
    payload = jwt.decode(token, SECRET)
    key = SSAGENT_KEY % payload.get('ssid')
    if not redis.exists(key):
      raise TokenRevoked('Token has been revoked')
    return payload
  except jwt.DecodeError:
    raise InvalidToken('Invalid token')
  except jwt.ExpiredSignatureError:
    raise Expired('Token has been expired')

def request_atk_by_rf(refresh_token):
  payload = decode_and_check(refresh_token)
  return make_access_token(payload.get('uid'), payload.get('ssid'))

def revoke(ssid):
  key = SSAGENT_KEY % ssid
  redis.delete(key)

def extend(refresh_token):
  payload = decode_and_check(refresh_token)
  return make_refresh_token(payload.get('uid'), payload.get('ssid'))

def sessions_of(uid):
  key = USSL_KEY % uid
  ssids = redis.lrange(key, 0, -1)
  keys = [SSAGENT_KEY % ssid for ssid in ssids]
  agents = redis.mget(keys)
  sslist = [{'ssid': ssids[i], 'agent': agents[i]} for i in range(len(keys))]
  return [s for s in sslist if __available_or_clean_up(s, key)]

def __available_or_clean_up(ss, key):
  if ss.get('agent'):
    return True
  redis.lrem(key, 0, ss)
  return False


## Decorator login required
def login_required(f):
  @wraps(f)
  def wraps_request(*args, **kwargs):
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
      payload = decode_and_check(access_token)
      request.uid = payload.get('uid')
      now = int(time.time())
      return f(*args, **kwargs) if now < payload.get('exp') else e401('Token has been expired')
    except InvalidToken:
      return e401('Invalid token, hack huh?')
    except Expired:
      return e401('Token has been expired')
    except TokenRevoked:
      return e401('Authentication has been revoked')
  return wraps_request

## this function should be place in other module, not this module
# wrap error handle
def e401(message):
  response.status = 401
  return dict(ok=False, message=message)

class InvalidToken(Exception):
  pass

class Expired(Exception):
  pass

class TokenRevoked(Exception):
  pass
