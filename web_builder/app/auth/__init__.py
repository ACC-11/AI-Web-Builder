from flask import Blueprint

bp = Blueprint('auth', __name__)

from web_builder.app.auth import routes