import sys
from importlib.util import module_from_spec, spec_from_loader
from importlib import invalidate_caches, reload, import_module
from http.server import BaseHTTPRequestHandler
import json
from inspect import getmembers, isfunction, getsource

# from api import test_module


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

        tests = load_tests()

        self._set_response()

        module_name = "module_under_test"

        module = create_module(code, module_name)

        message = "fine"

        try:
            exec(tests, {"add": module.add})
        except AssertionError:
            message = "ruh roh"

        self.wfile.write(message.encode("utf-8"))


def create_module(code, module_name):

    if module_name in sys.modules:
        print("deleting module")
        del sys.modules[module_name]

    spec = spec_from_loader(module_name, loader=None)
    module = module_from_spec(spec)

    exec(code, module.__dict__)
    sys.modules[module_name] = module

    return module


def load_tests():

    with open("./api/test_module.py") as f:
        return f.read()


#     return """
# def test_add_two_numbers():
#     global add
#     actual = add(3, 5)
#     expected = 8
#     assert actual == expected

# test_add_two_numbers()

#         """


# def run_tests():
#     from api import test_module

#     members = getmembers(test_module, isfunction)

#     for member in members:
#         print(member)
#         if member[0].startswith("test_"):
#             try:
#                 member[1]()
#             except AssertionError:
#                 print("oh noes")
#                 return "error"
