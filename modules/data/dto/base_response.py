import json


class BaseResponse:
    """
    This is the base response file which should be extended by all responses
    """

    def __init__(self, code, reason):
        """
        constructor for base response
        :param code: status code - 200, 404, 500 etc.
        :param reason:
        """
        self.code = code
        self.reason = reason

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)