from code_tester import test_code


code = """
def add(a, b):
    return a - b

"""

result = test_code(code)

print("result", result)
