# coding:utf-8
from flask import session, request
from flask.ext.socketio import join_room, leave_room
from .. import socketio
from ..wsy_redis_socketio import emit


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    msg = {
        'room': room,
        'msg': session.get('name') + ' : ' + message
    }
    emit('say', msg)


@socketio.on('exit', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
