from flask import Blueprint

med_search = Blueprint('med_search', __name__)

from . import views
