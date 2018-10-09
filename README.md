# Testing software: An overview

## This talk

Writing tests in Python with `pytest`.

Slides and sample tests: [github.com/carletes/ci-testing-talk](https://github.com/carletes/ci-testing-talk)

## Next talk

Continuous integration: Running tests

---

## pytest

A testing framework for Python code: https://docs.pytest.org/en/latest/

Tests look like this:

```python
# tests/test_simple.py

def divide(a, b):
    return a / b


def test_divide_works_for_integers():
    assert divide(4, 2) == 2


def test_divide_works_for_floats():
    assert divide(4.0, 2.0) == 2.0

```

---

## pytest: Running tests

You run tests like this:

```
$ pytest tests/test_simple.py
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 1 item

tests/test_simple.py ..                                                [100%]

========================== 2 passed in 0.04 seconds =========================
$ echo $?
0
$
```

---

## pytest: Failures (1)

How do test failures look like?

```python
# tests/_test_failures.py

def divide(a, b):
    return a / b


def test_integer_division():
    assert divide(1, 2) == 0.5
```

---

## pytest: Failures (2)

```
$ pytest tests/_test_failures.py
============================ test session starts ============================

platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 1 item

tests/_test_failures.py F                                               [100%]

================================= FAILURES ==================================
___________________________ test_integer_division ___________________________

    def test_integer_division():
>       assert divide(1, 2) == 0.5
E       assert 0 == 0.5
E        +  where 0 = divide(1, 2)

tests/_test_failures.py:6: AssertionError
========================= 1 failed in 0.08 seconds ==========================
$ echo $?
1
$
```

---

## Testing multiple things (1)

```python
# tests/test_parametrized.py

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
```

---

## Testing multiple things (2)

```
$ pytest tests/test_paremtrized.py
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 4 items

tests/test_paremtrized.py ....                                         [100%]

========================= 4 passed in 0.06 seconds ==========================
$
```
---

## Testing multiple things (3)

Another example: a sorting function

```python
# tests/sort.py

def sort(lst):
    if not lst:
        return lst

    head, tail = lst[0], lst[1:]
    return (sort([a for a in tail if a <= head]) +
            [head] +
            sort([a for a in tail if a > head]))

```

---

## Testing multiple things (4)

Use *test fixtures* to avoid repeating test samples:

```python
# tests/test_sort.py

import pytest

from sort import sort


@pytest.fixture
def lst():
    return [1, 2, 3]


def test_length(lst):
    assert len(sort(lst)) == len(lst)


def test_idempotence(lst):
    assert sort(sort(lst)) == sort(lst)
```

---

## Testing multiple things (XX)

Real world example: EFAS layers

https://tinyurl.com/y9mmqo4g

---

## Testing for errors (1)

Testing code that raises errors:

```
$ python
Python 2.7.10 (default, Oct  6 2017, 22:29:07)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> def divide(a, b):
...     return a / b
...
>>> divide(1, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in divide
ZeroDivisionError: integer division or modulo by zero
>>>
```

---

## Testing for errors (2)

Ensure the right error was raised with `pytest.raises()`:

```python
# tests/test_errors.py

import pytest


def divide(a, b):
    return a / b


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError) as exc:
        divide(1, 0)

    assert str(exc.value) == 'integer division or modulo by zero'
```

---

## pytest: Skipping tests

MARS is down for maintenance every Wednesday, so don't bother running
tests which need it on Wednesdays

```python
# tests/test_mars.py

from datetime import datetime

import pytest


def mars_retrieve(request):
    # A Python function that calls MARS ...
    return 'some GRIB data'


@pytest.mark.skipif(datetime.today().weekday() == 2, reason='MARS might be down')
def test_mars_access():
    assert mars_retrieve('RETRIEVE, DATE=-1') == 'some GRIB data'
```

---

## pytest: Skipping tests (2)

```
$ date
Mon  8 Oct 2018 18:07:06 BST
$ pytest tests/test_mars.py
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 1 item

tests/test_mars.py .                                                   [100%]

========================== 1 passed in 0.01 seconds =========================
$ echo $?
0
$
```

---

## pytest: Skipping tests (3)

```
$ date
Wed 10 Oct 2018 18:07:06 BST
$ pytest tests/test_mars.py
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 1 item

tests/test_mars.py s                                                   [100%]

========================= 1 skipped in 0.04 seconds =========================
$ echo $?
0
$
```

---

## Testing external dependencies (1)

Testing a function that retrieves URLs:

```python
# tests/test_get_url.py

import requests


def get_url(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content


def test_get_url():
    assert get_url('https://www.ecmwf.int/')
```

What happens when http://www.ecmwf.int is down?

---

## Testing external dependencies (2)

Bring your own web server!

```python
# tests/test_get_url2.py

import requests


def get_url(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.content


def test_get_url(webserver):
    res = get_url(webserver.url('/README.md'))
    assert 'Bring your own web server!' in res
```

---

## Testing external dependencies (3)

```python
# conftest.py

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
```

---

## Testing external dependencies (4)

Real world example: EFAS

https://tinyurl.com/ycneonl6

---

## Next talk: Continuous integration (CI): What?

Run your tests:

* automatically
* after every single change

in order to spot problems as early as possible

---

## Next talk: Continuous integration (CI): How?

You need:

* Tests.
* A CI infrastructure.

---

## We already have a test suite!

```
$ pytest tests
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 10 items

tests/test_errors.py .                                                 [ 10%]
tests/test_get_url.py .                                                [ 20%]
tests/test_get_url2.py .                                               [ 30%]
tests/test_mars.py .                                                   [ 40%]
tests/test_parametrized.py ....                                        [ 80%]
tests/test_simple.py ..                                                [100%]

========================= 10 passed in 0.49 seconds =========================
$ echo $?
0
$
```

---

## We already have a test suite (on Wednesdays)!

```
$ date
Wed 10 Oct 2018 20:29:32 BST
$ pytest tests
============================ test session starts ============================
platform darwin -- Python 2.7.10, pytest-3.8.2, py-1.6.0, pluggy-0.7.1
rootdir: /Users/carlos/src/ci-testing-talk, inifile:
collected 10 items

tests/test_errors.py .                                                 [ 10%]
tests/test_get_url.py .                                                [ 20%]
tests/test_get_url2.py .                                               [ 30%]
tests/test_mars.py s                                                   [ 40%]
tests/test_parametrized.py ....                                        [ 80%]
tests/test_simple.py ..                                                [100%]

==================== 9 passed, 1 skipped in 0.32 seconds ====================
$ echo $?
0
$
```

---

## ... we're only missing a CI infrastructure

Like our Bamboo build plan for EFAS:

https://software.ecmwf.int/builds/browse/WREP-WEBDEVEFAS
