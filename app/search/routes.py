from flask import render_template, current_app, request, url_for, redirect, flash, session, jsonify
from flask_login import login_required
from app import db
from app.search import bp
from app.search.es_search import addToIndex, removeFromIndex, queryIndex


@bp.before_app_request
def checkForElasticsearch():
    if current_app.elasticsearch.ping:
        print("Connected NOW!!")
        print(current_app.elasticsearch.info())
    else:
        print("Not connected NOW!!")

@bp.route('/')
@login_required
def index():
    return render_template('search/index.html.j2')
