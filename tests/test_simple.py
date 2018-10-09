def divide(a, b):
    return a / b


def test_divide_works_for_integers():
    assert divide(4, 2) == 2


def test_divide_works_for_floats():
    assert divide(4.0, 2.0) == 2.0
