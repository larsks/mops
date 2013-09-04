#!/usr/bin/python

import os
import sys
import logging
import datetime
import pprint

import pystache
import markdown
import yaml
import requests
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
log = None

def setup():
    global config
    global log

    log = logging.getLogger('mops')

    data_dir = os.environ['OPENSHIFT_DATA_DIR']
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

def redirect_on_error(url, status_codes=None):

    def redirect_decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except requests.exceptions.HTTPError as detail:
                if status_codes is None or \
                        detail.response.status_code in status_codes:
                    redirect(url)
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

            template = fetch_template(viewname)
            return markdown.markdown(
                    pystache.render(template, data))

        return wrapper

    return view_decorator

@route('/')
@view('index')
@redirect_on_error('/authorize', [401])
def index():
    if not 'moves_access_token' in request.session:
        redirect('/authorize')

    from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y%m%d')
    to_date = datetime.datetime.now().strftime('%Y%m%d')

    context = {
            'session': request.session,
            'profile': request.api.sub('user').sub('profile').get(),
            'summary': pprint.pformat(
                request.api.sub('user').sub('summary').sub(
                    'daily').get(**{'from': from_date, 'to': to_date}))
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
@redirect_on_error('/authorize', [400,401])
def login():
    if 'code' in request.query:
        log.info('getting token')
        token = request.moves_auth.get_access_token(request.query.code)
        request.session['moves_access_token'] = token
        log.info('redirecting back to main page')
        redirect('/')

@route('/info')
@view('info')
def info():
    return {
            'curdir': os.path.abspath(os.curdir),
            'config': config,
            'session': request.session,
            }

@route('/api/gpx/<date>')
@redirect_on_error('/authorize', [401])
def togpx (date):
    storyline = request.api.sub('user').sub('storyline').sub(
            'daily').sub(date).get(trackPoints=true)
    return storyline

if __name__ == '__main__':
    import bottle
    setup()
    bottle.run(app, host='localhost', port=8080)

