import pytest
from calculator import add_numbers, subtract, multiply, divide


def test_add():
    assert add_numbers(2, 3) == 6


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(3, 4) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
