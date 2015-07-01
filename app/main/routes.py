import json
from functools import wraps
from flask import make_response
from flask import session, redirect, url_for, render_template, request, jsonify, current_app
from . import main
from .forms import LoginForm

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers ="Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

@main.route('/', methods=['GET', 'POST'])
def index():
    app = current_app._get_current_object()
    return app.send_static_file('index.html')

@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)


@main.route('/login', methods=['POST'])
@allow_cross_domain
def login():
    print('post run!')
    name = request.form.get('name', '')
    room = request.form.get('room', '')
    if name == '' or room == '':
        return jsonify(data={'status': 'error'})
    session['name'] = name
    session['room'] = room
    return jsonify(data={'status': 'success'})

@main.route('/test', methods=['POST'])
@allow_cross_domain
def test():
    name = session.get('name')
    return jsonify(data={'status': name})