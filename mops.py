#!/usr/bin/python

import os
import sys
from bottle import route, default_app

app = default_app()

@route('/')
def index():
    return 'This is a test.'

