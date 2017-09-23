from flask import Blueprint

settings_app = Blueprint('settings', __name__)

from . import views