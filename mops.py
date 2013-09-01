#!/usr/bin/python

import os
import sys
from bottle import route

app = bottle.default_app()

route('/')
def index():
    return 'This is a test.'

