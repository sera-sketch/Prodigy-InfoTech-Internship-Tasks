import redis

# Connect to local Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

try:
    r.ping()
    print("Redis Connected Successfully ✅")
except redis.ConnectionError:
    print("Redis Connection Failed ❌")