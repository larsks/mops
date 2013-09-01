#!/usr/bin/python

import os
import sys
import pystache
import markdown
import yml
from bottle import Bottle

pagecache = {}
app = Bottle()
config = None

def setup():
    global config

    data_dir = os.environ['OPENSHIFT_DATA_DIR']
    config = yaml.load(os.path.join(
        data_dir, 'moves.yml'))

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

@app.route('/')
@view('index')
def index():
    return {}

@app.route('/info')
@view('info')
def cwd():
    return {
            'curdir': os.path.abspath(os.curdir),
            'client id': config['client id'],
            }

if __name__ == '__main__':
    import bottle
    bottle.run(app, host='localhost', port=8080)

