import json
import threading

from Database.Database import Database
from SQLiteErrorCods import *
from ConstantStorage import *

from flask import Flask, request, render_template, jsonify, flash, session, redirect, url_for
from pathlib import Path


class Server:

    # Инициализация сервера
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__, static_folder=str((Path(Path.cwd()) / ".." / "Frontend" / "static").resolve()),
                         template_folder=str((Path(Path.cwd()) / ".." / "Frontend" / "templates").resolve()))
        self.database = Database()
        # Описывает действия при открытие ссылки
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_shop)
        self.app.add_url_rule('/shop', view_func=self.get_shop)
        self.app.add_url_rule(
            '/registration', methods=['POST', 'GET'],
            view_func=self.get_registration)  # Описывает действия при открытие ссылки + разрешенные методы
        self.app.add_url_rule('/authorization', methods=['POST', 'GET'], view_func=self.get_authorization) 
        self.app.add_url_rule('/clear-database', view_func=self.clear_database)

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

    def get_shop(self):
        return render_template("main.html")  # Отобразить данную страницу

    def get_registration(self):
        if request.method == "POST":  # Если пришли данные методом POST
            # Получение данных формы регистрации
            data = request.json
            try:
                if data[REQUEST_TYPE] == REGISTRATION:  # Тип регистрации
                    # Упаковка ответа от БД и конвертация в JSON
                    return json.dumps(self.response_forming(self.registration(data)))
                # Тип проверки уникальности имени или почты
                elif data[REQUEST_TYPE] == EMAIL or data[REQUEST_TYPE] == NICKNAME:
                    if data[REQUEST_TYPE] == EMAIL:
                        return json.dumps(self.response_forming(self.database.check_for_uniqueness(EMAIL, data[TEXT_ANSWER])))
                    else:
                        # Упаковка ответа от БД и конвертация в JSON
                        return json.dumps(self.response_forming(self.database.check_for_uniqueness(NICKNAME, data[TEXT_ANSWER])))
                return str(ERROR_CODE)
            except Exception:
                return [ERROR_CODE, get_code_info(ERROR_CODE)]
        else:
            return render_template("registration_panel.html")

    def get_authorization(self):
        return render_template("authorization_panel.html")

    # Очистка базы данных
    def clear_database(self):
        self.database.clear_table("Users")
        return redirect("/")

    # Отправка данных в БД
    def registration(self, data):
        try:
            # session["userLogged"] = data[NICKNAME]
            data = (data[NICKNAME], data[EMAIL], data[PASSWORD])
            database_answer = self.database.add_data_to_table(data)
            if database_answer[0] == OK_CODE or database_answer[0] == ERROR_CODE:
                return database_answer
            elif database_answer[0] == UNIQUE_FIELD_ERROR_CODE:
                return [UNIQUE_FIELD_ERROR_CODE, database_answer[1].split(";")]
        except Exception:
            return [ERROR_CODE, get_code_info(ERROR_CODE)]

    # Формирование ответа серверу JSON
    def response_forming(self, database_answer):
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


if __name__ == '__main__':
    server_host = SERVER_HOST
    server_port = int(SERVER_PORT)
    server = Server(host=server_host, port=server_port)
    server.run_server()
