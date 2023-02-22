import json
import unicodedata

class ResponseAPI(object):
    SUCCESS = 'success'
    FAIL= 'fail'
    FORBIDDEN = 'forbidden'
    ERROR= 'error'
    UNAUTHORIZED = 'unauthorized'

    def __init__(self, status, message, data=None) -> None:
        self.status = status
        self.message = message
        self.data = data
    
    def __new__(cls, status, message, data=None):
        status_code = {"success":200, "fail":400, "forbidden":403, "error":500, "unauthorized":401}
        object = {"status": status, "message": message}
        if data:
            try:
                object["data"] = data
                json.dumps(object)
            except:
                object["data"] = json.loads(str(data))
        return (
            json.dumps(object),
            status_code[status],
            {"Content-Type": "application/json; charset=utf-8"}
        )

def normalize_string(string):
    string_normalize = unicodedata.normalize("NFD", string.lower())
    string_normalize = string_normalize.encode("ascii", "ignore")
    string_normalize = string_normalize.decode("utf-8")
    return string_normalize