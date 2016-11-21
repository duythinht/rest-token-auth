import auth, jwt, time
from fixtures import users
from qcore.asserts import *
from connection import redis

def test_before():
  [redis.delete(key) for key in redis.keys('auth:*')]

def test_ssid_():
  Lina = users.get_by_name('lena')
  ssid = auth.new_ssid(Lina.get('uid'), 'Fake Agent')
  assert_is_instance(ssid, str)
  key = auth.SSAGENT_KEY % ssid
  assert_eq(redis.exists(key), True)
  assert_eq(redis.exists(key), True)
  assert_eq(redis.ttl(key), 86400 * 60, 60)

def test_exp_make():
  next_time = auth.exp_time_for(5)
  assert_eq(next_time, int(time.time() + 5 * 60))

def test_make_refresh_token():
  Lina = users.get_by_name('lena')
  ssid = auth.new_ssid(Lina.get('uid'), 'Fake Agent')
  refresh_token = auth.make_refresh_token(Lina.get('uid'), ssid)
  payload = jwt.decode(refresh_token, auth.SECRET)
  assert_eq(payload.get('uid'), Lina.get('uid'))
  assert_eq(payload.get('ssid'), ssid)
  assert_eq(payload.get('exp'), auth.exp_time_for(86400))

def test_make_access_token():
  Lina = users.get_by_name('lena')
  ssid = auth.new_ssid(Lina.get('uid'), 'Fake Agent')
  token = auth.make_access_token(Lina.get('uid'), ssid)
  payload = jwt.decode(token, auth.SECRET)
  assert_eq(payload.get('uid'), Lina.get('uid'))
  assert_eq(payload.get('ssid'), ssid)
  assert_eq(payload.get('exp'), auth.exp_time_for(15))

def test_auth_for_user():
  Lina = users.get_by_name('lena')
  atk, rtk = auth.for_user(Lina.get('uid'), 'Agent')
  assert_eq(auth.decode_and_check(atk).get('uid'), Lina.get('uid'))
  assert_eq(auth.decode_and_check(rtk).get('uid'), Lina.get('uid'))

def test_request_access_token_by_rf():
  Lina = users.get_by_name('lena')
  ssid = auth.new_ssid(Lina.get('uid'), 'Fake Agent')
  refresh_token = auth.make_refresh_token(Lina.get('uid'), ssid)

  access_token = auth.request_atk_by_rf(refresh_token)

  payload = jwt.decode(access_token, auth.SECRET)
  assert_eq(payload.get('uid'), Lina.get('uid'))
  assert_eq(payload.get('ssid'), ssid)
  assert_eq(payload.get('exp'), auth.exp_time_for(15))

def test_invalid_rf_when_request_access_token():
  rf = 'what the fuck is this'
  with AssertRaises(auth.InvalidToken):
    access_token = auth.request_atk_by_rf(rf)


def test_expired_rf_when_request_access_token():
  xao_cho_rf = jwt.encode(dict(uid=1, ssid='hello', exp=(time.time()-1)), auth.SECRET)
  with AssertRaises(auth.Expired):
    atk = auth.request_atk_by_rf(xao_cho_rf)

def test_of_session_list():
  Adolf = users.get_by_name('adolf')
  ssid1 = auth.new_ssid(Adolf.get('uid'), 'Chrome')
  ssid2 = auth.new_ssid(Adolf.get('uid'), 'Android')
  ssid3 = auth.new_ssid(Adolf.get('uid'), 'Android')
  redis.delete(auth.SSAGENT_KEY % ssid3)

  sslist = auth.sessions_of(Adolf.get('uid'))
  assert_is_instance(sslist, list)
  assert_eq(len(sslist), 2)
  assert_eq(sslist[0].get('agent'), 'Chrome')
  assert_eq(sslist[1].get('agent'), 'Android')

  # clean after test
  redis.delete(auth.SSAGENT_KEY % ssid1)
  redis.delete(auth.SSAGENT_KEY % ssid2)

def test_revoked_raising_exception():
  Adolf = users.get_by_name('adolf')
  ssid = auth.new_ssid(Adolf.get('uid'), 'Chrome')
  token = auth.make_access_token(Adolf.get('uid'), ssid)
  redis.delete(auth.SSAGENT_KEY % ssid)
  with AssertRaises(auth.TokenRevoked):
    auth.decode_and_check(token)


def test_revove():
  Adolf = users.get_by_name('adolf')
  ssid = auth.new_ssid(Adolf.get('uid'), 'Chrome')
  key = auth.SSAGENT_KEY % ssid
  assert_eq(redis.exists(key), True)
  auth.revoke(ssid)
  assert_eq(redis.exists(key), False)

def test_after():
  [redis.delete(key) for key in redis.keys('auth:*')]
