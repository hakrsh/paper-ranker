from flask import Flask, render_template, request, redirect
from flask_paginate import Pagination
from db import get_papers
from rank_mapper import insert_conf_ranks
import time

# ----------------------Flask App----------------------------------

app = Flask(__name__)
app.secret_key = "secret key"
posts = []

def get_posts(posts, offset=0, per_page=10):
    return posts[offset: offset + per_page]


# insert_conf_ranks()

posts = []
time_taken = 0
@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/search', methods=['POST', 'GET'])
def search():
    global posts
    global time_taken
    if 'query' in request.form and request.form['query']:
        query = request.form['query']
        # remove extra while space from query
        query = query.strip().lower()
        query = ' '.join(query.split())
        query = query.replace(' ', '+')
        start = time.time()
        posts = get_papers(query, 1000)
        ranks_order = ['A*', 'A', 'B', 'C', 'NA']
        end = time.time()
        time_taken = end - start
        if len(posts) >0:
            posts.sort(key = lambda ele: ranks_order.index(ele["rank"]))
    # page, per_page, offset = get_page_args()
    if len(posts) == 0:
        return redirect('/')

    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page
    total = len(posts)
    pagination_posts = get_posts(posts, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('result.html',
                           posts=pagination_posts,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           time_taken=round(time_taken, 2),
                           count = len(posts)
                           )
if __name__ == "__main__":
    app.run(debug=True)
