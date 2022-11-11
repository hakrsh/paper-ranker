import logging
import requests
from rank_mapper import get_rank
ranks = {'A*', 'A', 'B', 'C', 'NA'}

def validate_json(json_data):
    if 'title' not in json_data or json_data['title'] == '':
        return False
    if 'authors' not in json_data:
        return False
    if 'venue' not in json_data or json_data['venue'] == '':
        return False
    if 'year' not in json_data or json_data['year'] is None or json_data['year'] == '':
        return False
    if 'url' not in json_data or json_data['url'] == '':
        return False
    return True

def fetch_dblp(topic, hit_count=100):
    url = "https://dblp.org/search/publ/api"
    params = {
        "q": topic,
        "h": hit_count,
        "format": "json"
    }
    res = requests.get(url, params=params)
    paper_list = list()

    try:
        data = res.json()
    except:
        logging.info('Error in fetching data from DBLP')
        return paper_list
    # get relevant data
    # check if key 'hit' exists in data['result']['hits']
    if 'hits' not in data['result']:
        return paper_list
    if 'hit' not in data['result']['hits']:
        return paper_list
    for entry in data['result']['hits']['hit']:
        paper_info = {}
        if 'info' not in entry or 'type' not in entry['info']:
            continue

        if entry['info']['type'] == 'Conference and Workshop Papers':
            if validate_json(entry['info']):
                paper_info['title'] = entry['info']['title']
                author_lst = list()
                auths = entry['info']['authors']['author']
                if isinstance(auths, dict):
                    author_lst.append(auths['text'])
                else:
                    for a in auths:
                        author_lst.append(a['text'])
                paper_info['authors'] = author_lst
                paper_info['venue'] = entry['info']['venue'].split()[0].lower()
                paper_info['year'] = entry['info']['year']
                paper_info['url'] = entry['info']['url']
                rank = get_rank(paper_info['venue'])
                if rank not in ranks:
                    logging.info('Rank not found for venue: ' + paper_info['venue'])
                    rank = 'NA'
                paper_info['rank'] = rank
                paper_list.append(paper_info)
    return paper_list


def fetch_semantic_scholar(topic,h):
    h = min(h,100)
    url = "http://api.semanticscholar.org/graph/v1/paper/search" 
    params = { 
        "query": topic,
        "limit": h,
        "fields": "title,authors,venue,year,url" 
    }     
    res = requests.get(url, params=params)
    paper_list = list()

    try:
        data = res.json()
    except:
        logging.info('Error in fetching data from Semantic Scholar')
        return paper_list
    for entry in data['data']:
        paper_info = {}
        if validate_json(entry):
            paper_info['title'] = entry['title']
            author_lst = list()
            for a in entry['authors']:
                if 'name' in a:
                    author_lst.append(a['name'])
            if len(author_lst) == 0:
                continue
            paper_info['authors'] = author_lst
            paper_info['venue'] = entry['venue']
            paper_info['year'] = entry['year']
            paper_info['url'] = entry['url']
            rank = get_rank(paper_info['venue'])
            if rank not in ranks:
                logging.info('Rank not found for venue: ' + paper_info['venue'])
                rank = 'NA'
            paper_info['rank'] = rank
            paper_list.append(paper_info)
    return paper_list
