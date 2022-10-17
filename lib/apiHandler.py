#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests.sessions import Session
from lib.logger import logger


class ApiHandle(object):

    def __init__(self, verify=False):
        self.session = Session()
        self.headers = {}
        self.verify = verify
        self.retry = 3

    def _request_handle(self, url, method='get', **kwargs):
        for idx in range(self.retry):
            try:
                result = getattr(self.session, method)(url,
                                                       verify=self.verify,
                                                       headers=self.headers,
                                                       **kwargs)
                return result
            except BaseException as err:
                logger.error(err)

    def get_url(self, url, **kwargs):
        response = self._request_handle(url, method='get', **kwargs)
        return response

    def post_url(self, url, **kwargs):
        response = self._request_handle(url, method='post', **kwargs)
        return response

    def _headers_handle(self, operation, headers, **kwargs):
        if operation == 'add':
            pass

    def set_headers(self, headers):
        self.headers = headers

    def add_headers(self, headers, update=True):
        for k, v in headers.items():
            if getattr(self.headers, k, False):
                if update:
                    self.headers[k] = v
            else:
                self.headers[k] = v

    def update_headers(self, headers):
        self.add_headers(headers)
