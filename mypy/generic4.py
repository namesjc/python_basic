from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self) -> None:
        self._store: Dict[str, T] = {}

    def set_itme(self, key: str, value: T) -> None:
        self._store[key] = value

    def get_item(self, key: str) -> T:
        return self._store[key]


if __name__ == "__main__":
    family_name_reg = Registry[str]()
    family_age_reg = Registry[int]()

    family_name_reg.set_itme("father", "John")
    family_name_reg.set_itme("mother", "Jane")

    family_age_reg.set_itme("father", 40)
    family_age_reg.set_itme("mother", "35")
