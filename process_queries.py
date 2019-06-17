#!/usr/bin/python

import sys
import pickle 
import time
import gzip
import json 

def load_dict(name):
    with open('obj_' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
    f.close()

def read_file(filename):
    with open(queries_file) as f:
        lines = [line.rstrip('\n') for line in f]
    f.close()
    return lines

start = time.time()
print('reading the identifier queries file ..')
queries_file = sys.argv[1]
queries = read_file(queries_file)
print('done')

print('reading the I_dict obj file ..')
I_dict = load_dict('I_dict')
print('done')

P_hist = dict()
for i_query in queries:
    if i_query in I_dict:
        for p in [x[1] for x in I_dict[i_query]]:
            if p in P_hist:
                P_hist[p] = P_hist[p] + 1
            else:
                P_hist[p] = 1

sorted_P_hist = sorted ( list(P_hist.items()), key=lambda x: x[1], reverse=True)
top_3_P = [x[0] for x in sorted_P_hist[:3]]
top_3_P_coverage = [ float(x[1])/len(queries) for x in sorted_P_hist[:3]]

print('--------------------------------------------------------')
print('top 3 P values and their coverage given the query file')
print('---')
for i,j in zip(top_3_P, top_3_P_coverage):
    print(i + "\t" + str(j))
print('---')

print('reading the gzipped json obj file')
with gzip.open('prop_idents_v6_nice.json.gz') as f:
    json_obj = json.load(f) 
print('done')

top_3_P_dicts = [ json_obj[P] for P in top_3_P ]

print('--------------------------------------------------------')

for i_query in queries:
    print('-----------')
    print(i_query)
    print('------')
    if len(top_3_P_dicts) > 0 and i_query in top_3_P_dicts[0]:
        print('top-1: ' + top_3_P[0] + ", " + top_3_P_dicts[0][i_query] + " cov: %.2f " % top_3_P_coverage[0])
    else:
        print('top-1: ' + 'NULL')
    if len(top_3_P_dicts) > 1 and i_query in top_3_P_dicts[1]:
        print('top-2: ' + top_3_P[1] + ", " + top_3_P_dicts[1][i_query]  + " cov: %.2f " % top_3_P_coverage[1])
    else:
        print('top-2: ' + 'NULL')
    if len(top_3_P_dicts) > 2 and i_query in top_3_P_dicts[2]:
        print('top-3: ' + top_3_P[2] + ", " + top_3_P_dicts[2][i_query] + " cov: %.2f " % top_3_P_coverage[2] )
    else:
        print('top-3: ' + 'NULL')

print('--------------------------------------------------------')
end = time.time()
total_time = end-start
print("time taken (query search): %.2f s" % total_time) 
print('--------------------------------------------------------')
