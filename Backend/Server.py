import json
import os
import threading

import werkzeug.security

from Database.Database import Database
from SQLiteErrorCods import *
from ConstantStorage import *
from Backend.User.UserLogin import UserLogin

from flask import Flask, request, render_template, session, redirect, url_for, g, make_response, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pathlib import Path


class Server:

    # Инициализация сервера
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__, static_folder=str((Path(Path.cwd()) / ".." / "Frontend" / "static").resolve()),
                         template_folder=str((Path(Path.cwd()) / ".." / "Frontend" / "templates").resolve()))
        self.login_manager = LoginManager(self.app)
        self.app.config["SECRET_KEY"] = "wefwefnuwi.owej88943rhjnfw.wefweiof.j9348hjfhjew"
        self.app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 10
        self.database = Database(os.path.join(self.app.root_path, "Database\\Users_database.db"))
        # Описывает действия при открытие ссылки
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.shop_page)
        self.app.add_url_rule('/shop', methods=['POST', 'GET'], view_func=self.shop_page)
        self.app.add_url_rule('/logout', view_func=self.logout)
        self.app.add_url_rule('/registration', methods=['POST', 'GET'],
                              view_func=self.registration_page)  # Описывает действия при открытие ссылки + разрешенные методы
        self.app.add_url_rule('/authorization', methods=['POST', 'GET'], view_func=self.authorization_page)
        self.app.add_url_rule('/upload_user_avatar', methods=['POST', 'GET'], view_func=self.upload_user_avatar)

        @self.app.before_request
        def before_request():
            self.database.get_db()

        @self.app.teardown_appcontext
        def teardown_appcontext(error):
            self.database.close_db()

        @self.login_manager.user_loader
        def load_user(user_id):
            return UserLogin().from_db(user_id, self.database)

        @self.login_manager.needs_refresh_handler
        @self.login_manager.unauthorized_handler
        def unauthorized():
            return redirect('/authorization')

    # Запуск сервера
    def run_server(self):
        self.server = threading.Thread(target=self.app.run(debug=True), kwargs={
            "host": self.host, "port": self.port})
        self.server.start()
        return self.server

    # Выключение сервера
    def shutdown(self):
        terminate_func = request.environ.get("werkzeug.server.shutdown")
        if terminate_func:
            terminate_func()
        return "shutdown"

    @login_required
    def logout(self):
        logout_user()  # Выход из профиля
        return redirect("/shop")

    @login_required
    def upload_user_avatar(self):
        if request.method == "POST":
            file = request.files[FILE]
            if file and current_user.verifyExt(file.filename):
                try:
                    img = file.read()
                    res = self.database.update_user_avatar(img, current_user.get_nickname())
                    if res[0] == ERROR_CODE:
                        return self.response_forming_code(ERROR_CODE)
                    else:
                        return self.response_forming_code(OK_CODE)
                except FileNotFoundError:
                    return self.response_forming_code(ERROR_CODE)
            else:
                return self.response_forming_code(ERROR_CODE)
        return redirect("/shop")

    def shop_page(self):
        if request.method == "POST":
            data = request.json
            try:
                if data[REQUEST_TYPE] == USER_INFO:  # Тип регистрации
                    arr_of_requested_data = data[REQUESTED_DATA]
                    answer = {
                        REQUEST_TYPE: USER_INFO,
                        REQUESTED_DATA: self.get_user_info(arr_of_requested_data)
                    }
                    print(answer)
                    return json.dumps(answer)
                return json.dumps(self.response_forming_code(ERROR_CODE))
            except BaseException:
                return json.dumps(self.response_forming_code(ERROR_CODE))
        return render_template("main.html")  # Отобразить данную страницу

    def registration_page(self):
        if request.method == "POST":  # Если пришли данные методом POST
            # Получение данных формы регистрации
            data = request.json
            try:
                if data[REQUEST_TYPE] == REGISTRATION:  # Тип регистрации
                    # Упаковка ответа от БД и конвертация в JSON
                    response = self.response_forming_from_db(self.registration(data))
                    if response[REQUEST_TYPE] == OK_CODE_ANSWER:
                        login_user(UserLogin().create(self.database.get_user_by_nickname(data[NICKNAME])),
                                   remember=True)  # Авторизация
                        return json.dumps(self.response_forming_code(OK_CODE))
                    res = make_response(json.dumps(response))
                    return res
                # Тип проверки уникальности имени или почты
                elif data[REQUEST_TYPE] == EMAIL or data[REQUEST_TYPE] == NICKNAME:
                    if data[REQUEST_TYPE] == EMAIL:
                        res = make_response(json.dumps(self.response_forming_from_db(
                            self.database.check_for_uniqueness(EMAIL, data[TEXT_ANSWER]))))
                        return res
                    else:
                        # Упаковка ответа от БД и конвертация в JSON
                        return json.dumps(self.response_forming_from_db(
                            self.database.check_for_uniqueness(NICKNAME, data[TEXT_ANSWER])))
                return json.dumps(self.response_forming_code(ERROR_CODE))
            except BaseException:
                return json.dumps(self.response_forming_code(ERROR_CODE))
        return render_template("registration_panel.html")

    def authorization_page(self):
        if request.method == "POST":  # Если пришли данные методом POST
            data = request.json
            try:
                if data[REQUEST_TYPE] == AUTHORIZATION:  # Тип авторизации
                    user = self.database.check_user_password(data[EMAIL], data[PASSWORD])  # Проверка пароля
                    if user:
                        login_user(UserLogin().create(user), remember=data[REMEMBER_ME])  # Авторизация
                        return json.dumps(self.response_forming_code(OK_CODE))
                    else:
                        return json.dumps(self.response_forming_code(USER_DOES_NOT_EXIT_ERROR_COD))
                return json.dumps(self.response_forming_code(ERROR_CODE))
            except BaseException as error:
                print(error)
                return json.dumps(self.response_forming_code(ERROR_CODE))
        elif current_user.get_id() is not None:
            return redirect("/shop")
        return render_template("authorization_panel.html")

    # Отправка данных в БД
    def registration(self, data):
        try:
            # session["userLogged"] = data[NICKNAME]
            data = (data[NICKNAME], data[EMAIL], werkzeug.security.generate_password_hash(data[PASSWORD]))
            database_answer = self.database.add_user(data)
            if database_answer[0] == OK_CODE or database_answer[0] == ERROR_CODE:
                return database_answer
            elif database_answer[0] == UNIQUE_FIELD_ERROR_CODE:
                return [UNIQUE_FIELD_ERROR_CODE, database_answer[1].split(";")]
        except Exception:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    # Формирование ответа серверу JSON
    @staticmethod
    def response_forming_from_db(database_answer):
        code = database_answer[0]
        if code == UNIQUE_FIELD_ERROR_CODE:  # Если ошибка уникальности, то возвращаем: тип, код, массив совпавших значений
            values = database_answer[1]
            answer = {
                REQUEST_TYPE: ERROR_CODE_ANSWER,
                CODE_ANSWER: code,
                VALUE_ANSWER: values
            }
        else:  # Иначе возвращаем: тип, код, текст
            text = database_answer[1]
            if code == OK_CODE:
                my_type = OK_CODE_ANSWER
            else:
                my_type = ERROR_CODE_ANSWER
            answer = {
                REQUEST_TYPE: my_type,
                CODE_ANSWER: code,
                TEXT_ANSWER: text
            }
        return answer

    @staticmethod
    def response_forming_code(code):
        if code == OK_CODE:
            my_type = OK_CODE_ANSWER
        else:
            my_type = ERROR_CODE_ANSWER
        answer = {
            REQUEST_TYPE: my_type,
            CODE_ANSWER: code,
            TEXT_ANSWER: get_code_info(code)
        }
        return answer

    @staticmethod
    def get_user_info(arr_of_requested_data):
        answer = {}
        if current_user.get_id() is not None:
            answer[IS_LOGIN] = True
            for data in arr_of_requested_data:
                if data == EMAIL:
                    answer[EMAIL] = current_user.get_email()
                elif data == NICKNAME:
                    answer[NICKNAME] = current_user.get_nickname()
                elif data == ACCOUNT_CREATION_TIME:
                    answer[NICKNAME] = current_user.get_account_creation_time()
                elif data == AVATAR:
                    answer[AVATAR] = current_user.get_avatar()
                    if not answer[AVATAR]:
                        answer[AVATAR] = ""
        else:
            answer[IS_LOGIN] = False
        return answer

    @staticmethod
    def redirect_to(url):
        answer = {
            REQUEST_TYPE: REDIRECT,
            TEXT_ANSWER: url
        }
        return answer


if __name__ == '__main__':
    server_host = SERVER_HOST
    server_port = int(SERVER_PORT)
    server = Server(host=server_host, port=server_port)
    server.run_server()
else:
    database = Database("Database\\Users_database.db")
    database.create_db()
