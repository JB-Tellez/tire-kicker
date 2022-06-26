from module_under_test import add


def test_add_two_numbers():
    actual = add(3, 5)
    expected = 8
    assert actual == expected
