import unittest
import sys
sys.path.append('/application')

import app.services.serialization as json
from app import config
from app import app

class TestBase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.configs = config.LocalConfig

        self.apiKey = self.configs.SECRET_KEY
        self.apiKeyHash = self.configs.SECRET_KEY_HASH

    def show_request(self, res):
        if res.status_code == 200:
            return {'status_code': res.status_code, **json.loads(res.data.decode('utf-8')) }
        else:
            return {'status_code': res.status_code} 

    def simulate_get(self, path, **kwargs):
        res = self.client.get(path, **kwargs, headers={'Content-Type': 'application/json', self.apiKey: self.apiKeyHash})
        return self.show_request(res)

    def simulate_post(self, path, **kwargs):
        res = self.client.post(path, **kwargs, headers={'Content-Type': 'application/json', self.apiKey: self.apiKeyHash})
        return self.show_request(res)

    def simulate_post(self, path, **kwargs):
        res = self.client.put(path, **kwargs, headers={'Content-Type': 'application/json', self.apiKey: self.apiKeyHash})
        return self.show_request(res)

    def simulate_post(self, path, **kwargs):
        res = self.client.delete(path, **kwargs, headers={'Content-Type': 'application/json', self.apiKey: self.apiKeyHash})
        return self.show_request(res)
