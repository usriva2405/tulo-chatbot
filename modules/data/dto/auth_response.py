from modules.data.dto.base_response import BaseResponse
import json


class AuthResponse(BaseResponse):

    def __init__(self, token, broker_list, code=200, reason="successful login"):
        self.token = token
        self.broker_list = broker_list
        self.code = code
        self.reason = reason

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)