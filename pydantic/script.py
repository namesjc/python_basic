from pydantic import BaseModel, field_validator
import datetime as dt


class Order(BaseModel):
    id: int
    item_name: str
    quantity: int
    create_at: dt.datetime
    delivered_at: dt.datetime | None = None

    # Config class is used to set the configuration of the model
    class Config:
        # validate_assignment is used to validate the assignment of the fields 
        validate_assignment = True

    @field_validator("quantity")
    def validate_quantity(cls, value: int) -> int:
        if value <= 1:
            raise ValueError("`quantity` must be greater than 0")
        return value

    @field_validator("create_at")
    def validate_create_at(cls, value: dt.datetime) -> dt.datetime:
        if value > dt.datetime.now():
            raise ValueError("`create_at` must be in the past")
        return value


if __name__ == "__main__":
    order = Order(
        id=1,
        item_name="apple",
        quantity=10,
        create_at=dt.datetime.now(),
        delivered_at=dt.datetime.now() + dt.timedelta(days=1),
    )
    order.quantity = -1  # raise ValueError
    print(order.quantity)
