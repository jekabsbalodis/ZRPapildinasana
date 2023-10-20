from flask import Blueprint

reg = Blueprint('reg', __name__)

from . import views