import json

from bussdcc.event import Event
from bussdcc.context import ContextProtocol
from bussdcc.runtime.sink import EventSink


class ConsoleSink(EventSink):
    def start(self, ctx: ContextProtocol) -> None:
        pass

    def stop(self) -> None:
        pass

    def handle(self, evt: Event) -> None:
        if not evt.time:
            return

        record = {
            "time": evt.time.isoformat(),
            "name": evt.name,
            "data": evt.data,
        }

        line = json.dumps(record, separators=(",", ":"))
        print(line)
