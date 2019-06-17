#!/usr/bin/python

import pickle
import json
import time
import gzip

def save_dict(obj, name):
    with open('obj_'+name+'.pkl','wb') as f:
         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL) 
    f.close()

start = time.time()
print('reading the gzipped json obj file')
with gzip.open('prop_idents_v6_nice.json.gz') as f:
    json_obj = json.load(f) 
print('done')

print('creating identifier dictionary .. ')
I_dict = dict()
for key in json_obj.keys(): 
    for k,v in json_obj[key].items():
        if k in I_dict:
            curr = I_dict[k]
            curr.append((v, key))
        else:
            curr = list()
            curr.append((v, key))
            I_dict[k] = curr
print('done..')

print('saving the dictionary on disk ..')
save_dict(I_dict, 'I_dict')
print('done')

end = time.time()
total_time = end-start
print("time taken ( preprocess): %.2f s" % total_time) 
