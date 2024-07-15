class Fruit:
    name: str
    grams: float
    cost_per_kg: float
    is_rare: InitVar[bool] = False
    similar_fruits: list[str] = field(default_factory=list)

    total_value: float = field(init=False)

    def __post_init__(self, is_rare) -> None:
        self.total_value = (self.grams / 1000) * self.cost_per_kg

        if is_rare:
            self.total_value *= 2
            self.cost_per_kg *= 2


def main() -> None:
    apple: Fruit = Fruit(name="Apple", grams=2500, cost_per_kg=1.5)
    print(apple)

    banana: Fruit = Fruit(name="Banana", grams=1500, cost_per_kg=10, is_rare=True)
    print(banana)

    orange: Fruit = Fruit(name="Orange", grams=500, cost_per_kg=2, similar_fruits=["Mandarin", "Tangerine"])
    print(orange)


if __name__ == "__main__":
    main()
