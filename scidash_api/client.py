from __future__ import unicode_literals, print_function
import json

import requests
from scidash_api import settings


class ScidashClient(object):

    """Base client class for all actions with Scidash API"""

    def __init__(self, config=None, build_info, hostname):
        self.token = None

        self.config = settings.CONFIG

        if config is not None:
            self.config.update(config)

    def get_headers(self):
        return {
                'Authorization': 'JWT {}'.format(self.token)
                }

    def login(self, username, password):
        """
        Getting API token from Scidash

        :param username:
        :param password:
        """
        credentials = {
                "username": username,
                "password": password
                }

        auth_url = self.config.get('auth_url')
        base_url = self.config.get('base_url')

        r = requests.post('{}{}'.format(base_url, auth_url), data=credentials)

        self.token = r.json().get('token')

        return self

    def upload_json(self, data, build_info=None, hostname=None):
        """
        Upload method for JSON string

        :param data: JSON string
        """
        return self._upload(data, build_info, hostname)

    def upload_object(self, _object, build_info=None, hostname=None):
        """
        Upload method for serializable object

        :param _object: dict or list
        """
        serialized_object = json.dumps(_object)

        return self._upload(serialized_object, build_info, hostname)

    def _upload(self, prepared_data, build_info, hostname):
        """
        Private main method for uploading

        :prepared_data: Prepared serialized data for uploading
        :returns: urllib3 requests object

        """

        prepared_data.get('test_instance').update({
            'build_info': build_info,
            'hostname': hostname
        })

        files = {
                'file': (self.config.get('file_name'), prepared_data)
                }

        headers = self.get_headers()

        upload_url = \
            self.config.get('upload_url') \
            .format(filename=self.config.get('file_name'))
        base_url = self.config.get('base_url')

        r = requests.put('{}{}'.format(base_url, upload_url), headers=headers,
                files=files)

        return r
