#!/usr/bin/python

import urllib
import requests
import logging

class APIError(Exception):
    pass

class Endpoint (object):
    def __init__(self, base_url, base=None):
        self.log = logging.getLogger('mops.rest.Endpoint')
        self.base_url = base_url

        if base is None:
            self.base = self
            self.session = requests.Session()
        else:
            self.base = base

    def unserialize(self, res):
        return res.json()

    def get(self, **params):
        return self.request(self.base.session.get, **params)
    def post(self, **params):
        return self.request(self.base.session.post, **params)

    def param_xform(self, v):
        return v

    def request(self, reqfunc, **params):
        for k,v in params.keys():
            xparams[k] = self.base.param_xform(v)

        res = reqfunc(self.url(), params=xparams)
        res.raise_for_status()
        return self.unserialize(res)

    def url(self, **params):
        url = self.base_url
        if params:
            url = url + '?' + urllib.urlencode(params)

        return url 

    def sub(self, k):
        new_base_url = '{}/{}'.format(self.base_url, k)
        return Endpoint(new_base_url, base=self.base)

if __name__ == '__main__':
    api = Endpoint('https://api.moves-app.com/api/v1')
    auth = Endpoint('https://api.moves-app.com/oauth/v1')

