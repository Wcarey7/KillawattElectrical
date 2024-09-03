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
        print('current_app WORKS!')
        current_app.elasticsearch.info()
        # Elasticsearch.info()

@bp.route('/')
@login_required
def index():
    # Elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})

    return render_template('base.html.j2')

# def index():
#     Elasticsearch.index(index='my_index', id=1, document={'text': 'this is a test'})
    

