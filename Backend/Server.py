import argparse
import threading

from Utils import config_parser
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy



class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_main)
        self.app.add_url_rule('/main', view_func=self.get_main)

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
        return render_template("main.html")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest="config")
    args = parser.parse_args()
    config = config_parser(args.config)
    server_host = config["SERVER_HOST"]
    server_port = int(config["SERVER_PORT"])
    server = Server(host=server_host, port=server_port)
    server.run_server()
