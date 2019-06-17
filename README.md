# isi-project

----
instructions to run: 

1. python preprocess_json.py 
2. python process_queries.py <query-file> 

step 1, reads the compressed json object in memory and creates a indicator dictionary (I_dict) containing indicator values as keys and list of (P-values, Q-values) as the values. Since this step is independent of the queries file, this is to be run once and the resulting I_dict is stored on disk. For efficiency, we can compress the I_dict pkl file, but currently it is uncompressed. 

step 2: I read the I_dict (created from step 1 for every query file) and check for coverage by constructing a histogram of P-values. I sort the histogram and take the top-3 as these indicate max coverage. I compute the coverage as freq of P-values in histogram / total # of queries. I read the compressed json file to and the top 3 P-dicts to construct the necessary output as specified in the readme of the challenge. 

For both steps 1 and 2, I report the time taken for the in-memory solution. 

Since step 1 is to be only run once, we can get some gains when we have to run with several query files (by taking a space-tradeoff hit, since we store the I_dict on disk)

----

output of the process_queries.py is present in sample1_output.txt (for input sample1.txt) and sample2_output.txt (for input sample2.txt) 

----

Here is the progress on the redis front. I have to tell upfront that this is a new thing to me, but looks like a very exciting technology to store and retrieve large blobs of data quickly. 

I went through the tutorial and soon found that redis does not natively support json objects. So the option was to either 1) use the json objects as strings and use the redis to efficiently store and retrieve these objects 2) decompose the nested json objects into something that can be used within redis. 

I then found this nice blogpost and video explaining a new module in redis called rejson. https://redislabs.com/blog/redis-as-a-json-store/ The video confirmed my hypothesis for the choices I have (if I do not have rejson). Then I decided to use rejson for it seems to be more flexible and provides performance improvements over both the above options as stated in the video. 

Then I figured out how to enable redis-json module in my redis server. Basically had to clone the redis-json repository (https://github.com/RedisJSON/RedisJSON), compile this and include the compiled .so file in the redis.conf and restart my local redis-server. 

I could even interface this with python and use the JSON.SET command from the python script. (https://pypi.org/project/rejson/). I am now at a point where I am a little stuck with 2 issues: 

1. jsonset is working but jsonget is returning empty when I try to get the object that I wrote to redis db before. However, I see this obj when I use the redis-cli and the JSON.get command there 

2. When I try the jsonset on the large json object from the file given in the programming challenge, I get a 'connection reset by peer' error message. Perhaps there is a setting that allows one to add large blobs of data to the redis db or something like that. 

---
