#!/usr/bin/python

import os
import sys
import pystache
import markdown
from bottle import Bottle

pagecache = {}
app = Bottle()

def fetch_template(viewname):
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

@app.route('/cwd')
@view('cwd')
def cwd():
    return { 'curdir': os.path.abspath(os.curdir) }

if __name__ == '__main__':
    import bottle
    bottle.run(app, host='localhost', port=8080)

