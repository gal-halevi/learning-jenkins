from calculator import add


def hello(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(hello("Gal"))
    print("2 + 3 =", add(2, 3))
