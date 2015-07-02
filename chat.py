#!/bin/env python
# coding:utf-8
from gevent import monkey
monkey.patch_all()
from app import create_app, socketio

app = create_app()

# def runapp(environ, start_response):
#     socketio.run(app, '0.0.0.0', 5000)

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 5000)
    # app.run(host='0.0.0.0')