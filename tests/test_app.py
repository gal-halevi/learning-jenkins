from app import hello


def test_hello():
    result = hello("Gal")
    assert result == "Hello, Gal!"
