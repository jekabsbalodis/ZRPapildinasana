from flask import Blueprint

filePrepare = Blueprint('filePrepare', __name__)

from . import views