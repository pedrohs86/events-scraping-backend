from flask import Flask
from flask_cors import CORS
from flask_script import Manager, Server

from src.config import APP_HOST, APP_PORT

def create():
    server = Flask(__name__)
    server.config['JSON_AS_ASCII'] = False
    from src.views import bp

    server.register_blueprint(bp)
    CORS(server)
    return server

def start():
    global server
    server = create()
    manager = Manager(server)
    manager.add_command("runserver", Server(host= APP_HOST, port=APP_PORT))
    manager.run()
    return server

server = create()