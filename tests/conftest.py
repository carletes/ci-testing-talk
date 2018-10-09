import multiprocessing
import subprocess

import pytest


def run_webserver():
    subprocess.Popen('python -m SimpleHTTPServer 8000', shell=True).wait()


class Webserver(object):

    def __init__(self):
        self.p = multiprocessing.Process(target=run_webserver)
        self.p.start()

    def stop(self):
        self.p.terminate()

    def url(self, path):
        return 'http://localhost:8000{}'.format(path)


@pytest.yield_fixture
def webserver():
    w = Webserver()
    yield w
    w.stop()
