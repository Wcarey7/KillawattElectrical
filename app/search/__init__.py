from flask import Blueprint, current_app

bp = Blueprint('search', __name__)

from app.search import routes


# if not current_app.elasticsearch:
#     print('NO')
# else:
#     print('YES')
#     print(current_app.elasticsearch.info())
