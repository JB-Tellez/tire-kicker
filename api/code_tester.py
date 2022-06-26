from importlib.util import module_from_spec, spec_from_loader
import sys
import pytest
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        code = """
def add(a, b):
    return a + b
        """
        self.wfile.write(code.encode())
        return


def test_code(code):

    module_name = "module_under_test"
    spec = spec_from_loader("module_under_test", loader=None)
    module = module_from_spec(spec)
    exec(code, module.__dict__)
    sys.modules[module_name] = module

    return pytest.main()
