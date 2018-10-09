import pytest

from sort import sort


@pytest.fixture(params=[
    ([], []),
    ([3, 2, 1], [1, 2, 3]),
    ([1, 1, 1], [1, 1, 1]),

])
def sample(request):
    return request.param


def test_sort(sample):
    lst, expected = sample
    assert sort(lst) == expected


def test_length(sample):
    lst, _ = sample
    assert len(sort(lst)) == len(lst)


def test_idempotence(sample):
    lst, _ = sample
    assert sort(sort(lst)) == sort(lst)
