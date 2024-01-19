from flask import Blueprint

file_prepare = Blueprint('file_prepare', __name__)

from . import views
