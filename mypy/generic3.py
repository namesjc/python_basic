from typing import Dict, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def get_first(container: Dict[K, V]) -> List[V]:
    return list(container.values())


if __name__ == "__main__":
    test: Dict[str, int] = {"a": 1, "b": 2, "c": 3}
    print(get_first(test))
