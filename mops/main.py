#!/usr/bin/python

import os
import sys
import logging
import datetime
import pprint

import markdown
import yaml
import requests
import beaker.middleware
import bottle
from bottle import hook, route, request, response, redirect

from . import moves
from . import templates
from .gpx import Storyline

data_dir = os.environ.get('OPENSHIFT_DATA_DIR', './data')

session_opts = {
    'session.type': 'file',
    'session.data_dir': os.path.join(data_dir, 'session/'),
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)
config = {}
log = None
views = templates.Templates('views')

def setup():
    global config
    global log

    log = logging.getLogger('mops')

    config = yaml.load(open(
        os.path.join(data_dir, 'moves.yml')))

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

    if 'client id' in config and 'client secret' in config:
        log.info('setting up moves_auth')
        request.moves_auth = moves.movesAuthEndpoint(
                config['client id'],
                config['client secret'])

    if 'moves_access_token' in request.session:
        log.info('found moves_access_token')
        request.api = moves.movesAPIEndpoint(
                request.session['moves_access_token'])

def redirect_on_error(statusmap):

    def redirect_decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except requests.exceptions.HTTPError as detail:
                if detail.response.status_code in statusmap:
                    redirect(statusmap[detail.response.status_code])
                else:
                    raise

        return wrapper

    return redirect_decorator

def view(viewname):

    def view_decorator(f):
        def wrapper(*args, **kwargs):
            data = f(*args, **kwargs)

            if not isinstance(data, dict):
                return data

            return markdown.markdown(views['{}.md'.format(viewname)].render(**data))

        return wrapper

    return view_decorator

@route('/')
@view('index')
@redirect_on_error({
    401: '/authorize',
    400: '/error',
    })
def index():
    if not 'moves_access_token' in request.session:
        redirect('/authorize')

    if 'from_date' in request.params:
        from_date = datetime.datetime.strptime(request.params['from_date'], '%Y%m%d')
    else:
        from_date = (datetime.datetime.now() - datetime.timedelta(days=7))

    if 'to_date' in request.params:
        to_date = datetime.datetime.strptime(request.params['to_date'], '%Y%m%d')
    else:
        to_date = (from_date + datetime.timedelta(days=7))

    context = {
            'session': request.session,
            'profile': request.api.sub('user').sub('profile').get(),
            'summary': request.api.sub('user').sub('summary').sub(
                    'daily').get(**{'from': from_date, 'to': to_date})
            }

    return context

@route('/error')
@view('error')
def error():
    return {}

@route('/authorize')
@view('authorize')
def authorize():
    return {
            'client_id': config['client id'],
            'scope': 'activity location'
            }

@route('/login')
@redirect_on_error({
    401: '/authorize',
    400: '/authorize',
    })
def login():
    if 'code' in request.query:
        log.info('getting token')
        token = request.moves_auth.get_access_token(request.query.code)
        request.session['moves_access_token'] = token
        log.info('redirecting back to main page')
        redirect('/')

@redirect_on_error({
    401: '/authorize',
    400: '/error',
    })
@route('/api/day/<date>.gpx')
def togpx (date):
    response.content_type = 'text/xml'
    response.headers['content-disposition'] = 'attachment; filename="{}.gpx"'.format(
            date)

    storyline = Storyline(
            request.api.sub('user').sub('storyline').sub(
            'daily').sub(date).get(trackPoints='true')
            )

    return storyline.asgpx()

@redirect_on_error({
    401: '/authorize',
    400: '/error',
    })
@route('/api/day/<date>.json')
def tojson (date):
    response.headers['content-disposition'] = 'attachment; filename="{}.json"'.format(
            date)

    return {'storyline': 
            request.api.sub('user').sub('storyline').sub(
                'daily').sub(date).get(trackPoints='true')}

if __name__ == '__main__':
    import bottle
    logging.basicConfig() 
    setup()
    bottle.run(app, host='localhost', port=8080)

