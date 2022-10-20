import threading
from api import *
import redis
import json

r = redis.Redis(host='redis-17459.c264.ap-south-1-1.ec2.cloud.redislabs.com',port=17459, password='w7R5evprtUnVOj9J9XZihOOvsVjpMEk7')

def quick_search(key, hits=10):
    paper_list = fetch_dblp(key, hits)
    if(paper_list):
        r.set(key, json.dumps(paper_list), ex=60*60*24)
    print('Quick search completed for key: ', key)
    return paper_list

def depth_search(key, hits=30):
    paper_list = fetch_dblp(key, hits)
    paper_list += fetch_semantic_scholar(key, hits)
    if paper_list:
        r.set(key, json.dumps(paper_list), ex=60*60*24)
    print('Depth search completed for key: ', key)

def get_papers(key, hits=30):
    if r.get(key):
        print('Cache hit!')
        return json.loads(r.get(key))
    else:
        print('Cache miss!')
        threading.Thread(target=depth_search, args=(key, hits)).start()
        return quick_search(key, 20)
