import threading
import json
import time
import redis 

r = redis.Redis(host='localhost', port=6379, db=0)

rank_map = dict()
def build_rank(file_name):
    with open(file_name) as f:
        for conf in json.load(f):
            rank = conf['Rank']
            conf_id = conf['Acronym'].lower()
            print(f'Inserting {conf_id} with rank {rank}')
            r.set(conf_id, rank)

def get_rank(conf_name):
    conf_name = conf_name.lower()
    rank = r.get(conf_name)
    print(f'Rank of {conf_name} is {rank}')
    if rank:
        return rank.decode('utf-8')
    else:
        return 'NA'
    
def insert_conf_ranks():
    if r.get('conf_ranks') == None:
        files = ['Ranks/rank1.json', 'Ranks/rank2.json', 'Ranks/rank3.json']
        print('Inserting Conference Ranks')
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

