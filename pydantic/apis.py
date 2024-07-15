import datetime as dt

import requests
from pydantic import BaseModel, Field

URL = "https://www.gov.uk/bank-holidays.json"


class Event(BaseModel):
    title: str
    date: dt.date
    notes: str
    bunting: bool

    @property
    # Check if the event has passed
    def is_passed(self):
        return self.date < dt.date.today()


class Division(BaseModel):
    name: str = Field(alias="division") # Rename the field
    events: list[Event]


class BankHolidays(BaseModel):
    england_and_wales: Division
    scotland: Division
    northern_ireland: Division

    class Config:
        # Convert the field names to snake_case
        alias_generator = lambda x: x.replace("_", "-")


if __name__ == "__main__":
    response = requests.get(URL)
    data = response.json()

    holidays = BankHolidays(**data)
    print(holidays.england_and_wales.events[0])
    print(holidays.scotland.events[-1].is_passed)
