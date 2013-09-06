#!/usr/bin/python

import jinja2

class Templates (object):
    def __init__ (self):
        self.environ = jinja2.Environment(
                loader=jinja2.PackageLoader('mops', 'views'))

    def __getitem__(self, k):
        return self.environ.get_template('{}.md'.format(k))

