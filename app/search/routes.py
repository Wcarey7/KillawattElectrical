from flask import render_template, current_app, request, url_for, redirect, flash, session, jsonify
from flask_login import login_required
from app import db
from app.search import bp
from elasticsearch import Elasticsearch
# from app.search.es_search import addToIndex, removeFromIndex, queryIndex


@bp.before_app_request
def checkForElasticsearch():
    if not current_app.elasticsearch:
    # if not Elasticsearch:
        print('current_app DOES NOT WORK!')
    else:
        myes = Elasticsearch
        print('current_app WORKS!')
        print('my es info: ' + str(current_app.elasticsearch.info()))
        # Elasticsearch.info()
        # print('my es info 1: '+ str(myes.info()))

@bp.route('/')
@login_required
def index():
    # Elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})

    return render_template('search/index.html.j2')

# def index():
#     Elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})
    

