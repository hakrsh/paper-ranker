from models import *
from api import *
import time
import threading


def insert_paper_new_design(key, paper_list):
    """
    key -> string eg machine learning
    paper_list -> list of dict
    dict fields -> id,title,year,authors(list),venue,rank,keyword(hash value)
    """
    # insert the papers into the database
    number_of_paper_already_in_db = 0
    number_of_new_inserts = 0
    number_of_key_updates = 0

    for paper in paper_list:
        pid = paper['id']
        # if id present in papers collection, update keywords
        temp = paper_collection.objects(pid=pid).first()
        if temp:
            # update keywords
            if paper['keyword'] not in temp.keywords:
                temp.keywords.append(paper['keyword'])
                temp.save()
                number_of_key_updates += 1
            # temp.keywords.append(paper['keyword'])
            # temp.save()
            number_of_paper_already_in_db += 1
        else:
            new_paper = paper_collection()
            new_paper.pid = paper['id']
            new_paper.title = paper['title']
            new_paper.year = int(paper['year'])
            new_paper.authors = paper['authors']
            new_paper.venue = paper['venue']
            new_paper.rank = paper['rank']
            new_paper.keywords.append(paper['keyword'])
            new_paper.url = paper['url']
            new_paper.save()
            number_of_new_inserts += 1
        # update keyword to paper id mapping
        temp = keyword_collection.objects(keyword=hash(key)).first()
        if temp:
            if paper['id'] not in temp.papers:
                temp.papers.append(paper['id'])
                temp.save()
                number_of_key_updates += 1
            # temp.papers.append(paper['id'])
            # temp.save()
        else:
            new_keyword = keyword_collection()
            new_keyword.keyword = hash(key)
            new_keyword.papers.append(paper['id'])
            new_keyword.save()
    print('Insertion Completed!')
    print(f'{number_of_paper_already_in_db} papers already in db')
    print(f'{number_of_key_updates} key updates')
    print(f'{number_of_new_inserts} new papers inserted')

def background_insertion(key, hits):
    print(f'Backgroud worker! fetching {key} papers From API')
    start = time.time()
    paper_list = bg_fetch_dblp(key, hits)
    paper_list += bg_fetch_semantic_scholar(key, hits)
    end = time.time()
    print(f'Total {len(paper_list)} papers fetched in {end-start} seconds')
    print('Background worker inserting to db')
    # create a new thread to insert the papers into the database
    t = threading.Thread(target=insert_paper_new_design,
                            args=(key, paper_list))
    t.start()

def get_papers(key, hits=30):
    temp = keyword_collection.objects(keyword=hash(key)).first()
    if temp:
        start = time.time()
        print(f'fetching {key} papers From DB')
        paper_list = list()
        for pid in temp.papers:
            paper_info = dict()
            temp = paper_collection.objects(pid=pid).first()
            paper_info['title'] = temp.title
            paper_info['year'] = temp.year
            paper_info['authors'] = temp.authors
            paper_info['venue'] = temp.venue
            paper_info['rank'] = temp.rank
            paper_info['url'] = temp.url
            paper_list.append(paper_info)
        end = time.time()
        print(f'Total {len(paper_list)} papers fetched in {end-start} seconds')
        threading.Thread(target=background_insertion,args=(key, hits)).start()
    else:
        print(f'fetching {key} papers From API')
        start = time.time()
        paper_list = fetch_dblp(key, hits)
        paper_list += fetch_semantic_scholar(key, hits)
        end = time.time()
        print(f'Total {len(paper_list)} papers fetched in {end-start} seconds')
        print('New thread is inserting to db')
        # create a new thread to insert the papers into the database
        t = threading.Thread(target=insert_paper_new_design,
                             args=(key, paper_list))
        t.start()
    return paper_list
