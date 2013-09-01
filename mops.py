#!/usr/bin/python

import os
import sys
from bottle import Bottle

app = Bottle()

@app.route('/')
def index():
    return 'This is a test.'

