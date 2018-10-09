from datetime import datetime

import pytest


def mars_retrieve(request):
    # A Python function that calls MARS ...
    return 'some GRIB data'


@pytest.mark.skipif(datetime.today().weekday() == 2, reason='MARS might be down')
def test_mars_access():
    assert mars_retrieve('RETRIEVE, DATE=-1') == 'some GRIB data'
