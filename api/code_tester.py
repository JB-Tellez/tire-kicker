from importlib.util import module_from_spec, spec_from_loader
import sys
import pytest
from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        payload = json.loads(post_data.decode())

        code = payload["code"]

        self._set_response()
        message = str(test_code(code))
        self.wfile.write(message.encode("utf-8"))

        print("all done")

        sys.exit()


def test_code(code):

    module_name = "module_under_test"
    spec = spec_from_loader("module_under_test", loader=None)
    module = module_from_spec(spec)
    exec(code, module.__dict__)
    sys.modules[module_name] = module

    result = pytest.main()

    return result
