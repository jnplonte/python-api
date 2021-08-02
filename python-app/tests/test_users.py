import json

from tests.base import TestBase

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class UserTest(TestBase):
    def setUp(self):
        super(UserTest, self).setUp()

        self.userKey = 'Lrzu8gKFu3Q9346pEgcE4eFBrFYsE95JS6Zsgecu6LFYa7yr2D'

    def tearDown(self):
        super(UserTest, self).tearDown()

    def test_get_user(self):
        res = self.simulate_get('/v1/core/users', query_string='user-key=' + self.userKey)

        self.assertEqual(res['status_code'], 200)
        self.assertEqual(res['status'], 'success')
        self.assertTrue(len(res['data']) >= 1)
