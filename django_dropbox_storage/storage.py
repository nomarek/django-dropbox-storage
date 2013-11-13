#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage

from dropbox.client import DropboxOAuth2FlowNoRedirect, DropboxClient
from dropbox.rest import ErrorResponse


class DropboxStorage(Storage):

    def __init__(self):
        flow = DropboxOAuth2FlowNoRedirect(settings.APP_KEY,
                                           settings.APP_SECRET)

        #authorize_url = flow.start()
        #access_token, user_id = flow.finish(settings.ACCESS_TOKEN)

        self.client = DropboxClient(settings.ACCESS_TOKEN)

    def _open(self, name, mode='rb'):
        return File(name, mode=mode)

    def _save(self, name, content):
        response = self.client.put_file(name, content, overwrite=True)
        return response['path']

    def delete(self, name):
        self.client.file_delete(name)

    def exists(self, name):
        try:
            self.client.metadata(name)
        except ErrorResponse as e:
            if e.status == 404:
                return False
            raise e
        return True

    def size(self, name):
        return self.client.metadata(name)['bytes']

    def url(self, name):
        return self.client.metadata(name)
