#!/usr/bin/python

import os
import sys
import pystache
import markdown
import yaml
import beaker.middleware
import bottle
from bottle import hook, route, request, response, redirect

import moves

session_opts = {
    'session.type': 'file',
    'session.data_dir': os.path.join(
        os.environ['OPENSHIFT_DATA_DIR'],
        'session/'),
    'session.auto': True,
}

pagecache = {}
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)
config = {}

def setup():
    global config

    data_dir = os.environ['OPENSHIFT_DATA_DIR']
    config = yaml.load(open(
        os.path.join(data_dir, 'moves.yml')))

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

    if 'client id' in config and 'client secret' in config:
        request.moves_auth = moves.movesAuthEndpoint(
                config['client id'],
                config['client secret'])

    if 'moves_access_token' in request.session:
        request.moves_api = moves.movesAPIEndpoint(
                request.session['token'])

def fetch_template(viewname):
    global pagecache

    if viewname in pagecache:
        return pagecache[viewname]

    text = open(
            os.path.join(
                'views', '{}.md'.format(viewname)
            )).read()
    pagecache[viewname] = text

    return text

def view(viewname):

    def view_decorator(f):
        def wrapper(*args, **kwargs):
            data = f(*args, **kwargs)

            if not isinstance(data, dict):
                return data

            template = fetch_template(viewname)
            return markdown.markdown(
                    pystache.render(template, data))

        return wrapper

    return view_decorator

@route('/')
@view('index')
def index():
    if not 'moves_access_token' in request.session:
        redirect('/authorize')

    context = {
            'session': request.session,
            'profile': request.session.moves_api.user.profile(),
            }

    return context

@route('/authorize')
@view('authorize')
def authorize():
    return {
            'client id': config['client id'],
            'scope': 'activity location'
            }

@route('/login')
def login():
    if 'code' in request.query:
        token = request.moves_auth.get_access_token(request.query.code)
        request.session['moves_access_token'] = token
        redirect('/')

@route('/info')
@view('info')
def info():
    return {
            'curdir': os.path.abspath(os.curdir),
            'config': config,
            'session': request.session,
            }

if __name__ == '__main__':
    import bottle
    setup()
    bottle.run(app, host='localhost', port=8080)

