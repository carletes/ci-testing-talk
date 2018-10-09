import pytest


def divide(a, b):
    return a / b


@pytest.mark.parametrize(
    'a, b, expected',
    [
        (4, 2, 2),
        (4.0, 2.0, 2.0),
        (1, 2, 0),
        (1, 2.0, 0.5),
    ]
)
def test_division(a, b, expected):
    assert divide(a, b) == expected
