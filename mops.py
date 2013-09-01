#!/usr/bin/python

import os
import sys
import pystache
import markdown
from bottle import Bottle

pagecache = {}
app = Bottle()

def fetch(view):
    if view in pagecache:
        return pagecache[view]

    text = open(
            os.path.join(
                'views', '{}.md'.format(view)
            )).read()
    pagecache[view] = text
    return text

@app.route('/')
def index():
    return markdown.markdown(pystache.render(fetch('index')))

@app.routue('/cwd')
def cwd():
    return os.curdir

