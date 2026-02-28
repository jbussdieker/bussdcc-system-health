from typing import Optional
from dataclasses import dataclass

from bussdcc.events import EventSchema


@dataclass(slots=True)
class AppBooted(EventSchema):
    name = "app.booted"

    app_name: str
    version: str


@dataclass(slots=True)
class AppShuttingDown(EventSchema):
    name = "app.shutting_down"

    version: str
    reason: Optional[str]
