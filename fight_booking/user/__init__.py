from flask import Blueprint

#  定義
from .model import Role
from fight_booking import db

user = Blueprint('user', __name__)
#  關聯
from . import view
from . import model
