import threading
import json
import time
import redis 
import logging
logging.basicConfig(level=logging.INFO)

r = redis.Redis(host='redis-17459.c264.ap-south-1-1.ec2.cloud.redislabs.com',port=17459, password='w7R5evprtUnVOj9J9XZihOOvsVjpMEk7')
if r.ping():
    logging.info('Connected to Redis')
else:
    logging.error('Redis connection failed')

rank_map = dict()
def build_rank(file_name):
    with open(file_name) as f:
        logging.info(f'Building Rank from {file_name}')
        for conf in json.load(f):
            rank = conf['Rank']
            conf_id = conf['Acronym'].lower()
            r.set(conf_id, rank)

def get_rank(conf_name):
    conf_name = conf_name.lower()
    rank = r.get(conf_name)
    if rank:
        return rank.decode('utf-8')
    else:
        return 'NA'
    
def insert_conf_ranks():
    if r.get('conf_ranks') == None:
        files = ['Ranks/rank1.json', 'Ranks/rank2.json', 'Ranks/rank3.json']
        start = time.time()
        threads = []
        for file_name in files:
            build_rank(file_name)
            threads.append(threading.Thread(target=build_rank, args=(file_name,)))
            threads[-1].start()
        for thread in threads:
            thread.join()
        print('Conference Rank Insertion Completed!')
        print(f'Total Time Taken: {time.time()-start} seconds')
        r.set('conf_ranks', 1)

