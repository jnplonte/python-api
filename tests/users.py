import falcon
import json

from . import base


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class TestRouting(base.TestBase):
    def setUp(self):
        super(TestRouting, self).setUp()
        self.entry_path = '/v1/users'

    def tearDown(self):
        super(TestRouting, self).tearDown()

    def testGetAllUsers(self):
        body = body = self.simulate_get(self.entry_path, query_string='test=true', headers={'Content-Type': 'application/json', 'x-python-api-key': '$someSecretKeyHere$'})
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['status'], 'success')
        self.assertEqual(body['message'], 'get-success')
