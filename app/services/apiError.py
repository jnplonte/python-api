from falcon.http_error import HTTPError
import app.services.serialization as json


class ApiError(HTTPError):
    def __init__(self, status, error):
        super(ApiError, self).__init__(status)
        self.status = status
        self.error = error

    def to_dict(self, obj_type=dict):
        super(ApiError, self).to_dict(obj_type)
        obj = self.error
        return json.loads(obj)