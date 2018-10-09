import requests


def get_url(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content


def test_get_url(webserver):
    res = get_url(webserver.url('/README.md'))
    assert 'Bring your own web server!' in res
