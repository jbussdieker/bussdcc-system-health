from dataclasses import dataclass

from bussdcc import Message


@dataclass(slots=True, frozen=True)
class Notify(Message):
    title: str
    message: str
