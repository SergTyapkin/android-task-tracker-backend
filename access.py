from functools import wraps
from flask import redirect, request, make_response
from database.database import *
import database.SQL_requests as sql
from utils import *


_config = read_config("config.json")
_DB = Database(_config)

HTTP_NOT_AUTHENTICATED = 401
HTTP_NO_PERMISSIONS = 403


def get_logined_userid():
    token = request.cookies.get('session_token')
    if not token:
        return ''
    session = _DB.execute(sql.selectUserIdBySessionToken, [token], dictionary=True)
    if len(session) == 0:
        return ''
    return session


def get_logined_user():
    token = request.cookies.get('session_token')
    if not token:
        return ''
    result = _DB.execute(sql.selectUserDataBySessionToken, [token], dictionary=True)
    if len(result) == 0:
        return None
    return result


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userData = get_logined_user()
        if not userData:
            return make_response("Не авторизован", HTTP_NOT_AUTHENTICATED)
        return f(*args, **kwargs, userData=userData)

    return wrapper


def login_required_return_id(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userid = get_logined_userid()
        if not userid:
            return make_response("Не авторизован", HTTP_NOT_AUTHENTICATED)
        return f(*args, **kwargs, userid=userid)

    return wrapper


def login_required_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userData = get_logined_user()
        if not userData:
            return make_response("Не авторизован", HTTP_NOT_AUTHENTICATED)
        if userData['isadmin']:
            return make_response("Нет прав", HTTP_NO_PERMISSIONS)
        return f(*args, **kwargs)

    return wrapper
