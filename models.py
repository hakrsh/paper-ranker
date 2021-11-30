from mongoengine import *
connect('paper-ranker')


class paper_collection(Document):
    pid = IntField()  # hash value
    title = StringField()
    year = IntField()
    authors = ListField(StringField())
    venue = StringField()
    rank = StringField()
    keywords = ListField(IntField())  # list of keyword hashes
    url = StringField()

# create a keyword to paper id mapping


class keyword_collection(Document):
    keyword = IntField()  # hash value
    papers = ListField(IntField())  # list of paper id (hash value)


# class Conference(Document):
#     conf_id = IntField()
#     rank = StringField()

# Run in terminal:
# db.paper_collection.createIndex({"pid":1}, {background:true})
# db.keyword_collection.createIndex({"keyword":1}, {background:true})
# db.Conference.createIndex({"conf_id":1}, {background:true})
