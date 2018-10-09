import pytest


def divide(a, b):
    return a / b


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError) as exc:
        divide(1, 0)

    assert str(exc.value) == 'integer division or modulo by zero'
