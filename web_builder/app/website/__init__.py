from flask import Blueprint

bp = Blueprint('website', __name__)

from web_builder.app.website import routes