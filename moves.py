#!/usr/bin/python

import requests
import urllib
import time
import logging

import rest

moves_api_base = 'https://api.moves-app.com/api/v1'
moves_oauth_base = 'https://api.moves-app.com/oauth/v1'

class movesAuthEndpoint (rest.Endpoint):
    def __init__(self, client_id, client_secret,
            base_url=moves_oauth_base,
            auth_code=None,
            token=None):

        super(movesAuthEndpoint, self).__init__(base_url)

        self.log = logging.getLogger('mops.moves')
        self.auth_code = auth_code
        self.client_id = client_id
        self.client_secret = client_secret
        self.session.params.update({
            'client_id': client_id,
            })

    def auth_url(self, scope='location activity'):
        return self.sub('authorize').url(
                response_type='code',
                client_id=self.client_id,
                scope=scope)

    def get_access_token(self, code):
        res = self.sub('access_token').post(
                grant_type='authorization_code',
                code=code,
                client_secret=self.client_secret,
                )

        if 'access_token' in res:
            self.log('got token = {}'.format(res['access_token']))

        return res

    def refresh_access_token(self, token):
        return self.sub('access_token').post(
                grant_type='refresh_token',
                refresh_token=token['refresh_token'],
                client_secret=self.client_secret,
                )

class movesAPIEndpoint (rest.Endpoint):
    def __init__(self, token, authorize_func, base_url=moves_api_base):
        super(movesAPIEndpoint, self).__init__(base_url)
        self.set_token(token)

    def set_token(self, token):
        self.token = token
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(token['access_token']),
            })

