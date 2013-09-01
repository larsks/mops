#!/usr/bin/python

import os
import sys
from bottle Bottle

app = Bottle()

@app.route('/')
def index():
    return 'This is a test.'

