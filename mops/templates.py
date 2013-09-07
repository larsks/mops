#!/usr/bin/python

import jinja2

class Templates (object):
    def __init__ (self, directory):
        self.environ = jinja2.Environment(
                loader=jinja2.PackageLoader('mops', directory))

    def __getitem__(self, k):
        return self.environ.get_template('{}'.format(k))

