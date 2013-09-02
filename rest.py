#!/usr/bin/python

import urllib
import requests

class APIError(Exception):
    pass

class Endpoint (object):
    def __init__(self, base_url, base=None):
        self.base_url = base_url

        if base is None:
            self.base = self
            self.session = requests.Session()
        else:
            self.base = base

    def __getattr__(self, k):
        new_base_url = '{}/{}'.format(self.base_url, k)
        return Endpoint(new_base_url, base=self.base)

    def __call__(self, method='GET', **params):
        if method == 'GET':
            method_func = self.base.session.get
        elif method == 'POST':
            method_func = self.base.session.post
        else:
            raise APIError('unsupported http method')

        res = method_func(self.url(), params=params)
        res.raise_for_status()
        return res

    def url(self, **params):
        url = self.base_url
        if params:
            url = url + '?' + urllib.urlencode(params)

        return url 

    def sub(self, k):
        return getattr(self, k)

if __name__ == '__main__':
    api = Endpoint('https://api.moves-app.com/api/v1')
    auth = Endpoint('https://api.moves-app.com/oauth/v1')

