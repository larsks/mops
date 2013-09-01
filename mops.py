#!/usr/bin/python

import os
import sys
import pystache
import markdown
import yaml
import beaker.middleware
import bottle
from bottle import hook, route, request, response, redirect

session_opts = {
    'session.type': 'file',
    'session.data_dir': os.path.join(
        os.environ['OPENSHIFT_DATA_DIR'],
        'session/'),
    'session.auto': True,
}

pagecache = {}
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)
config = None

def setup():
    global config

    data_dir = os.environ['OPENSHIFT_DATA_DIR']
    config = yaml.load(open(
        os.path.join(data_dir, 'moves.yml')))

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

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
    request.session['visited'] = True
    return {}

@route('/authorize')
@view('authorize')
def authorize():
    return {
            'client id': config['client id'],
            'scope': 'activity location'
            }

@route('/info')
@view('info')
def info():
    return {
            'curdir': os.path.abspath(os.curdir),
            'config': config,
            'session': request.session,
            'client id': config['client id'],
            }

if __name__ == '__main__':
    import bottle
    bottle.run(app, host='localhost', port=8080)

