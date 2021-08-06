import json
import os
import threading

from Database.Database import Database
from Backend.SQLiteErrorCods import *
from Backend.ConstantStorage import *

from flask import Flask, request, render_template, jsonify, flash, session, redirect, url_for
from pathlib import Path


class Server:

    # Инициализация сервера
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__, static_folder="C:\\Users\\Vemarus\\Unity\\Online_store2\\Frontend\\static", template_folder="C:\\Users\\Vemarus\\Unity\\Online_store2\\Frontend\\templates")
        self.database = Database("Users_database.db")
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)  # Описывает действия при открытие ссылки
        self.app.add_url_rule('/', view_func=self.get_shop)
        self.app.add_url_rule('/shop', view_func=self.get_shop)
        self.app.add_url_rule(
            '/registration', methods=['POST', 'GET'], view_func=self.get_registration)  # Описывает действия при открытие ссылки + разрешенные методы
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

    def shutdown_server_button(self):
        request.get(f'http://{self.host}:{self.port}/shutdown')

    def get_shop(self):
        return render_template("main.html")

    def get_registration(self):
        if request.method == "POST":
            try:
                data = request.get(DATA_FROM_SERVER)  # Получение данных формы регистрации
                data = json.loads(data.text)  # Перевод данных из JSON
                if data is dict:
                    if data[REQUEST_TYPE] == REGISTRATION:  # Тип регистрации
                        database_answer = self.registration(data)
                        code = database_answer[0]
                        text = database_answer[1]
                        if code == OK_CODE:
                            answer = {
                                REQUEST_TYPE: OK_CODE_ANSWER,
                                CODE_ANSWER: code,
                                TEXT_ANSWER: text
                            }
                        else:
                            answer = {
                                REQUEST_TYPE: ERROR_CODE_ANSWER,
                                CODE_ANSWER: code,
                                TEXT_ANSWER: text
                            }
                        return json.dumps(answer)
                    elif data[REQUEST_TYPE] == EMAIL or data[REQUEST_TYPE] == NICKNAME:  # Тип проверки уникальности имени или почты
                        if data[REQUEST_TYPE] == EMAIL:
                            database_answer = self.database.check_for_uniqueness(EMAIL, data[KEY])
                        else:
                            database_answer = self.database.check_for_uniqueness(NICKNAME, data[KEY])
                        code = database_answer[0]
                        text = database_answer[1]
                        if code == OK_CODE:
                            answer = {
                                REQUEST_TYPE: OK_CODE_ANSWER,
                                CODE_ANSWER: code,
                                TEXT_ANSWER: text
                            }
                        else:
                            answer = {
                                REQUEST_TYPE: ERROR_CODE_ANSWER,
                                CODE_ANSWER: code,
                                TEXT_ANSWER: text
                            }
                        return json.dumps(answer)
                return str(ERROR_CODE)
            finally:
                return str(ERROR_CODE)
        else:
            return render_template("registration_panel.html")

    def clear_database(self):
        self.database.clear_table("Users")
        return redirect("/")

    # Отправка данных в БД
    def registration(self, data):
        try:
            # session["userLogged"] = data[NICKNAME]
            data = (data[NICKNAME], data[EMAIL], data[PASSWORD])
            answer = self.database.add_data_to_table(data)
            if answer[0] == OK_CODE:
                return str(OK_CODE)
            elif answer[0] == UNIQUE_FIELD_ERROR_CODE:
                return f"{str(UNIQUE_FIELD_ERROR_CODE)}:{answer[1]}"
            else:
                return str(ERROR_CODE)
        finally:
            return str(ERROR_CODE)


if __name__ == '__main__':
    server_host = SERVER_HOST
    server_port = int(SERVER_PORT)
    server = Server(host=server_host, port=server_port)
    server.run_server()
