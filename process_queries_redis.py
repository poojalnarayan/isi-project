#!/usr/bin/python

import redis
import json
import gzip
import time

redis_host = "localhost"
redis_port = 6379
redis_password = ""

start = time.time()
print('reading the gzipped json obj file')
with gzip.open('prop_idents_v6_nice.json.gz') as f:
    json_obj = json.load(f) 
print('done')
end_json = time.time()

print("time taken ( read json): %.2f s" % (end_json - start)) 

print('writing json objects to a redis database ..')
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

start_redis = time.time()
for idx, k in enumerate(json_obj.keys()):
    if idx % 5 == 0:
        end_redis = time.time()
        print('completed ' + str(idx) + ' obj. :' + str(end_redis - start_redis))
        start_redis = time.time()
    r.execute_command('JSON.SET', k, '.', json.dumps(json_obj[k]))

#r.execute_command('JSON.SET', 'object', '.', json.dumps(json_obj))
print('done.')
end = time.time()

print("time taken ( write redis): %.2f s" % (end - end_json)) 
total_time = end-start
print("time taken ( total): %.2f s" % total_time) 
#reply = json.loads(r.execute_command('JSON.GET', 'object'))
