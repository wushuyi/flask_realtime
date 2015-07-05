# coding:utf-8
from flask import Flask
# from flask.ext.socketio import SocketIO
from .flask_redis_socketio import WsySocketIO as SocketIO

socketio = SocketIO()


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    # app.config['DEBUG'] = True

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

