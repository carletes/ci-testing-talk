import requests


def get_url(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content


def test_get_url():
    assert get_url('https://www.ecmwf.int/')
