from flask import current_app
# from elasticsearch import Elasticsearch


# def addToIndex():
#     if not current_app.elasticsearch:
#         return
#     output = {}
#     current_app.elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})

# def removeFromIndex():


# def queryIndex(index, query):
#     if not current_app.elasticsearch:
#         return
#     search = current_app.elasticsearch.search(index="my_index", query={"match_all": {}})
#     print(search)
