import pytest

from sort import sort


@pytest.fixture
def lst():
    return [1, 2, 3]


def test_length(lst):
    assert len(sort(lst)) == len(lst)


def test_idempotence(lst):
    assert sort(sort(lst)) == sort(lst)
