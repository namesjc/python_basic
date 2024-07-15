from typing import List, TypeVar

T = TypeVar("T", str, int)


def first(container: List[T]) -> T:
    print(container)
    return "a"


if __name__ == "__main__":
    list1: List[int] = [1, 2, 3]
    print(first(list1))

    list2: List[str] = ["a", "b", "c"]
    print(first(list2))
