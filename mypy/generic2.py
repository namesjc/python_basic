from typing import Dict, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def get_item(key: K, container: Dict[K, V]) -> V:
    return container[key]


if __name__ == "__main__":
    test: Dict[str, int] = {"a": 1, "b": 2, "c": 3}
    print(get_item("a", test))
    print(get_item("b", test))

