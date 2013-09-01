#!/usr/bin/python

import os
import sys
from bottle import Bottle, run

app = Bottle()

app.route('/')
def index():
    return 'This is a test.'

