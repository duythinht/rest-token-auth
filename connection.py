import redis as py_redis
import os

redis = py_redis.StrictRedis(host=os.environ.get('REDIS_HOST', '10.60.3.31'))
