from api import *
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def get_papers(key, hits=30):

    if r.get(key):
        print('Cache hit!')
        return json.loads(r.get(key))
    else:
        print('Cache miss!')
        paper_list = fetch_dblp(key, hits)
        paper_list += fetch_semantic_scholar(key, hits)
        r.set(key, json.dumps(paper_list))
        return paper_list   
