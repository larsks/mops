#!/usr/bin/python

import requests
import urllib
import time
import logging
import datetime

from . import rest

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

    def param_xform(self, v):
        if isinstance(datetime.datetime, v):
            v = v.strftime('%Y%m%d')

        return v

    def auth_url(self, scope='location activity'):
        return self.sub('authorize').url(
                response_type='code',
                client_id=self.client_id,
                scope=scope)

    def get_access_token(self, code):
        return self.sub('access_token').post(
                grant_type='authorization_code',
                code=code,
                client_secret=self.client_secret,
                client_id=self.client_id,
                )

    def refresh_access_token(self, token):
        return self.sub('access_token').post(
                grant_type='refresh_token',
                refresh_token=token['refresh_token'],
                client_secret=self.client_secret,
                client_id=self.client_id,
                )

    def check_access_token(self, token):
        return self.sub('tokeninfo').get(
                access_token=token['access_token'])

class movesAPIEndpoint (rest.Endpoint):
    def __init__(self, token, base_url=moves_api_base):
        super(movesAPIEndpoint, self).__init__(base_url)
        self.set_token(token)

    def set_token(self, token):
        self.token = token
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(token['access_token']),
            })

    def param_xform(self, v):
        if isinstance(datetime.datetime, v):
            v = v.strftime('%Y%m%d')

        return v

