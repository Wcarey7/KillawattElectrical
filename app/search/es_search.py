from flask import current_app, jsonify
from app.search import bp


@bp.route("/ping/")
def ping():
    if current_app.elasticsearch.ping:
        return "THIS IS CONNECTED"
    

def addToIndex(id, index_name, content):
    if not current_app.elasticsearch:
        return
    output = {}
    # current_app.elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})
    current_app.elasticsearch.index(index=index_name, id=id, document=content)
    # return jsonify(status='200 OK', message='Index add successful')
    return

# def removeFromIndex():


# def queryIndex(index, query):
#     if not current_app.elasticsearch:
#         return
#     search = current_app.elasticsearch.search(index="my_index", query={"match_all": {}})
#     print(search)
