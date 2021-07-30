import threading

from werkzeug.utils import redirect

from Utils import config_parser
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop.db'
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.database = SQLAlchemy(self.app)
        self.database.create_all()
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_main)
        self.app.add_url_rule('/main', view_func=self.get_main)
        self.app.add_url_rule('/registration', methods=['POST', 'GET'], view_func=self.get_registration)

    def run_server(self):
        self.server = threading.Thread(target=self.app.run(debug=True), kwargs={"host": self.host, "port": self.port})
        self.server.start()
        return self.server

    def shutdown(self):
        terminate_func = request.environ.get("werkzeug.server.shutdown")
        if terminate_func:
            terminate_func()
        return "shutdown"

    def shutdown_server_button(self):
        request.get(f'http://{self.host}:{self.port}/shutdown')

    def get_main(self):
        items = Item.query.order_by(Item.id).all()
        return render_template("main.html", data=items)

    def get_registration(self):
        if request.method == "POST":
            name = request.form['name']
            surname = request.form['surname']
            patronymic = request.form['patronymic']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            item = Item(name=name, surname=surname, patronymic=patronymic, email=email, password=password,
                        gender=True)
            try:
                database.session.add(item)
                database.session.commit()
                return redirect('/')
            except():
                return "ERROR"
        else:
            return render_template("index.html")


# if __name__ == '__main__':
# parser = argparse.ArgumentParser()
# parser.add_argument('--config', type=str, dest="config")
# args = parser.parse_args()
# config = config_parser(args.config)
config = config_parser('C:\\Users\\Vemarus\\Desktop\\Shop\\config.txt')
server_host = config["SERVER_HOST"]
server_port = int(config["SERVER_PORT"])
server = Server(host=server_host, port=server_port)
database = server.database


class Item(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    surname = database.Column(database.String, nullable=False)
    patronymic = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    password = database.Column(database.String, nullable=False)
    gender = database.Column(database.Boolean, default=True)

    def __repr__(self):
        return f'{self.id} - {self.surname} ; '


print(Item.query.all())
server.run_server()
