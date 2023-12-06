from flask import Blueprint

medSearch = Blueprint('medSearch', __name__)

from . import views