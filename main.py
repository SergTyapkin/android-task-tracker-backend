from flask import Flask, request, jsonify, make_response
import uuid
from datetime import datetime, timedelta
from database.database import *
import database.SQL_requests as sql
from access import *

from utils import *

app = Flask(__name__)
config = read_config("config.json")
DB = Database(config)

HTTP_INVALID_DATA = 400
HTTP_INVALID_AUTH_DATA = 401
HTTP_NOT_AUTHENTICATED = 403
HTTP_NOT_FOUND = 404
HTTP_ALREADY_REGISTERED = 409
HTTP_INTERNAL_ERROR = 500
HTTP_OK = 200


def new_session(resp):
    tokenResp = DB.execute(sql.selectSessionById, [resp['id']], dictionary=True)
    if len(tokenResp) > 0:
        token = tokenResp['token']
        expires = tokenResp['expires']
    else:
        token = str(uuid.uuid4())
        expires = (datetime.now() + timedelta(seconds=24 * 60 * 60)).strftime("%Y-%m-%d %H:%M:%S")  # 24 * 60 * 60 = 1 day
        DB.execute(sql.insertSession, [resp['id'], token, expires])

    res = make_response(jsonify(resp))
    res.set_cookie("session_token", token, expires=expires)
    return res


@app.route('/')
def home():
    return "Это начальная страница API, а не сайт. Вiйди отсюда!"


@app.route("/user/auth", methods=["POST"])
def userAuth():
    try:
        requestJson = request.form
        username = requestJson['username']
        password = requestJson['password']
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.selectUserByNamePassword, [username, password], dictionary=True)
    if len(resp) == 0:
        return make_response("Неверные логин или пароль", HTTP_INVALID_AUTH_DATA)

    return new_session(resp)


@app.route("/user/session", methods=["DELETE"])
def userSessionDelete():
    token = request.cookies.get('session_token')
    if not token:
        return make_response("Вы не вошли в аккаунт", HTTP_NOT_AUTHENTICATED)

    try:
        DB.execute(sql.deleteSessionByToken, [token])
    except:
        return make_response("Сессия не удалена", HTTP_INTERNAL_ERROR)

    return make_response("Вы вышли из аккаунта")


@app.route("/user", methods=["GET"])
@login_required
def userGet(userData):
    return make_response(jsonify(userData))


@app.route("/user", methods=["POST"])
def userCreate():
    try:
        requestJson = request.form
        name = requestJson['name']
        password = requestJson['password']
        university = requestJson['university']
        educationGroup = requestJson['educationGroup']
        groupRole = requestJson['groupRole']
        avatarUrl = requestJson['avatarUrl'] if requestJson['avatarUrl'] else None
        email = requestJson['email'] if requestJson['email'] else None
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    try:
        resp = DB.execute(sql.insertUser, [name, password, university, educationGroup, groupRole, avatarUrl, email],
                          dictionary=True)
    except:
        return make_response("Имя пользователя или email заняты", HTTP_INVALID_DATA)

    return new_session(resp)


@app.route("/user/<string:username>/confirmation", methods=["PUT"])
@login_required_admin
def userUpdateConfirmation(username):
    try:
        requestJson = request.form
        university = requestJson['university']
        educationGroup = requestJson['educationGroup']
        groupRole = requestJson['groupRole']
        isConfirmed = requestJson['groupRole']
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    resp = DB.execute(sql.updateUserConfirmationByName, [university, educationGroup, groupRole, isConfirmed, username],
                      dictionary=True)
    if len(resp) == 0:
        return make_response("Имя пользователя не найдено", HTTP_NOT_FOUND)

    return make_response("Успешно обновлено")


@app.route("/user/<string:username>/email", methods=["PUT"])
@login_required
def userUpdateEmail(username, userData):
    try:
        requestJson = request.form
        email = requestJson['email']
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if (userData['name'] != username) and (not userData['isadmin']):
        return make_response("Нет прав", HTTP_NO_PERMISSIONS)

    resp = DB.execute(sql.updateUserEmailByName, [email, username], dictionary=True)
    if len(resp) == 0:
        return make_response("Имя пользователя не найдено", HTTP_NOT_FOUND)

    return make_response("Успешно обновлено")


@app.route("/user/<string:username>/password", methods=["PUT"])
@login_required
def userUpdatePassword(username, userData):
    try:
        requestJson = request.form
        oldPassword = requestJson['oldPassword']
        newPassword = requestJson['newPassword']
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if (userData['name'] != username) and (not userData['isadmin']):
        return make_response("Нет прав", HTTP_NO_PERMISSIONS)

    resp = DB.execute(sql.updateUserPasswordByNamePassword, [newPassword, username, oldPassword], dictionary=True)
    if len(resp) == 0:
        return make_response("Имя пользователя не найдено, или имя пользователя или пароль не подходят", HTTP_NOT_FOUND)

    return make_response("Успешно обновлено")


@app.route("/user/<string:username>/avatar", methods=["PUT"])
@login_required
def userUpdateAvatar(username, userData):
    try:
        requestJson = request.form
        image = requestJson['image']
    except:
        return make_response("Не удалось сериализовать json", HTTP_INVALID_DATA)

    if (userData['name'] != username) and (not userData['isadmin']):
        return make_response("Нет прав", HTTP_NO_PERMISSIONS)

    resp = DB.execute(sql.updateUserAvatarByName, [image, username], dictionary=True)
    if len(resp) == 0:
        return make_response("Имя пользователя не найдено", HTTP_NOT_FOUND)

    return make_response("Успешно обновлено")


if __name__ == '__main__':
    app.run(port=config['api_port'])
