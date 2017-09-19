from flask import Blueprint

home_app = Blueprint('home', __name__)

from . import views