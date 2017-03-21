from flask import Blueprint
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from flask import g


api = Blueprint('api', __name__)
auth_basic = HTTPBasicAuth()
auth_token = HTTPTokenAuth('Bearer')


@auth_basic.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return user.verify_password(password)


@auth_token.verify_token
def verify_token(token):
    user = User.verify_auth_token(token, 2592000)
    if not user:
        return False
    g.user = user
    return True


@auth_basic.error_handler
@auth_token.error_handler
def auth_error():
    return 'Please log in first!'

from . import views
