__author__ = 'wushuyi'
from socketio.namespace import BaseNamespace
from flask.ext.socketio import _SocketIOMiddleware, SocketIO, \
    emit, send, join_room, leave_room, close_room, disconnect
from flask import request
import json
import redis

rc = redis.StrictRedis()
pubsub = rc.pubsub()


class WsySocketIO(SocketIO):
    def _get_namespaces(self, base_namespace=BaseNamespace):

        class GenericNamespace(base_namespace):
            socketio = self
            base_emit = base_namespace.emit
            base_send = base_namespace.send

            def initialize(self):
                self.rooms = set()
                self.pubsub = pubsub
                self.pubsub.subscribe('default')
                self.spawn(self.listener)

            def listener(self):
                for item in self.pubsub.listen():
                    if item['type'] == 'message':
                        res = json.loads(item['data'])
                        if item['channel'] == 'default':
                            self.emit(res['1'], res['2'])
                        else:
                            self.emit(res['1'], res['2'], item['channel'])

            def process_event(self, packet):
                if self.socketio.server is None:
                    self.socketio.server = self.environ['socketio'].server
                message = packet['name']
                args = packet['args']
                app = self.request
                return self.socketio._dispatch_message(app, self, message, args)

            def join_room(self, room):
                if self.socketio._join_room(self, room):
                    self.rooms.add(room)
                    self.pubsub.subscribe(room)

            def leave_room(self, room):
                if self.socketio._leave_room(self, room):
                    self.rooms.remove(room)
                    self.pubsub.unsubscribe(room)

            def close_room(self, room):
                self.socketio._close_room(self, room)
                self.pubsub.unsubscribe(room)

            def recv_connect(self):
                if self.socketio.server is None:
                    self.socketio.server = self.environ['socketio'].server
                ret = super(GenericNamespace, self).recv_connect()
                app = self.request
                self.socketio._dispatch_message(app, self, 'connect')
                return ret

            def recv_disconnect(self):
                if self.socketio.server is None:
                    self.socketio.server = self.environ['socketio'].server
                app = self.request
                self.socketio._dispatch_message(app, self, 'disconnect')
                self.socketio._leave_all_rooms(self)
                return super(GenericNamespace, self).recv_disconnect()

            def recv_message(self, data):
                if self.socketio.server is None:
                    self.socketio.server = self.environ['socketio'].server
                app = self.request
                return self.socketio._dispatch_message(app, self, 'message',
                                                       [data])

            def recv_json(self, data):
                if self.socketio.server is None:
                    self.socketio.server = self.environ['socketio'].server
                app = self.request
                return self.socketio._dispatch_message(app, self, 'json',
                                                       [data])

            def emit(self, event, *args, **kwargs):
                ns_name = kwargs.pop('namespace', None)
                broadcast = kwargs.pop('broadcast', False)
                room = kwargs.pop('room', None)
                if broadcast or room:
                    if ns_name is None:
                        ns_name = self.ns_name
                    return self.socketio.emit(event, *args, namespace=ns_name,
                                              room=room)
                if ns_name is None:
                    return self.base_emit(event, *args, **kwargs)
                return request.namespace.socket[ns_name].base_emit(event, *args,
                                                                   **kwargs)

            def send(self, message, json=False, ns_name=None, callback=None,
                     broadcast=False, room=None):
                if broadcast or room:
                    if ns_name is None:
                        ns_name = self.ns_name
                    return self.socketio.send(message, json, ns_name, room)
                if ns_name is None:
                    return request.namespace.base_send(message, json, callback)
                return request.namespace.socket[ns_name].base_send(message,
                                                                   json,
                                                                   callback)

            def disconnect(self, silent=False):
                self.socketio._leave_all_rooms(self)
                return super(GenericNamespace, self).disconnect(silent)

        namespaces = dict((ns_name, GenericNamespace)
                          for ns_name in self.messages)
        return namespaces

def emit(event, *args, **kwargs):
    room = kwargs.pop('room', None)
    msg = {}
    msg['1'] = event
    msg['2'] = args[0]
    data = json.dumps(msg)
    # print msg
    if room:
        rc.publish(room, data)
    else:
        rc.publish('default', data)