from flask import Blueprint

bp = Blueprint('fts_search', __name__)

from app.fts_search import routes
