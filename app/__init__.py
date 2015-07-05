# coding:utf-8
from flask import Flask
# from flask.ext.socketio import SocketIO
from .wsy_redis_socketio import WsySocketIO as SocketIO
from flask.ext.kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from simplekv.decorator import PrefixDecorator
from .redis_link import rc

store = RedisStore(rc)
prefixed_store = PrefixDecorator('sessions_', store)
socketio = SocketIO()
kvsession = KVSessionExtension()


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    # app.config['DEBUG'] = True

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    kvsession.init_app(app, prefixed_store)
    return app

