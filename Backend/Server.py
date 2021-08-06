import threading

from werkzeug.utils import redirect
from Database.Database import Database
# from Backend.SQLiteErrorCods import *

from SQLiteErrorCods import *
from pathlib import Path
from Utils import config_parser
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__, static_folder=str(Path(Path.cwd(), "Frontend", "static")),
                         template_folder=str(Path(Path.cwd(), "Frontend", "templates")))
        self.database = Database("Users_database.db")
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_shop)
        self.app.add_url_rule('/shop', view_func=self.get_shop)
        self.app.add_url_rule(
            '/registration', methods=['POST', 'GET'], view_func=self.get_registration)
        self.app.add_url_rule('/clear-database', view_func=self.clear_database)

    def run_server(self):
        self.server = threading.Thread(target=self.app.run(debug=True), kwargs={
                                       "host": self.host, "port": self.port})
        self.server.start()
        return self.server

    def shutdown(self):
        terminate_func = request.environ.get("werkzeug.server.shutdown")
        if terminate_func:
            terminate_func()
        return "shutdown"

    def shutdown_server_button(self):
        request.get(f'http://{self.host}:{self.port}/shutdown')

    def get_shop(self):
        items = self.database.get_all_data()
        return render_template("main.html", data=items)

    def get_registration(self):
        if request.method == "POST":
            try:
                nickname = request.form.get('nickname')
                email = request.form.get('email')
                password = request.form.get('password')
                if nickname.strip() != "" and email.strip() != "" and password.strip() != "":
                    data = (nickname, email, password)
                    answer = self.database.add_data_to_table(data)
                    if answer[0] == OK_COD:
                        return str(OK_COD)
                    elif answer[0] == UNIQUE_FIELD_ERROR_COD:
                        return f"{str(UNIQUE_FIELD_ERROR_COD)}:{answer[1]}"
                    else:
                        return str(ERROR_COD)
                else:
                    return str(ERROR_COD)
            except():
                return str(ERROR_COD)
        else:
            return render_template("registration_panel.html")

    def clear_database(self):
        self.database.clear_table("Users")
        return redirect("/")


# if __name__ == '__main__':
# parser = argparse.ArgumentParser()
# parser.add_argument('--config', type=str, dest="config")
# args = parser.parse_args()
# config = config_parser(args.config)
config = config_parser(str(Path(Path.cwd(), "Backend", "config.txt")))
server_host = config["SERVER_HOST"]
server_port = int(config["SERVER_PORT"])
server = Server(host=server_host, port=server_port)
server.run_server()
