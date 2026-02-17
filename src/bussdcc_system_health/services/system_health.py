from pathlib import Path

from bussdcc.context import ContextProtocol
from bussdcc.service import Service


class SystemHealthService(Service):
    name = "system_health"
    interval = 5.0

    def __init__(self) -> None:
        pass

    def tick(self, ctx: ContextProtocol) -> None:
        self._emit_throttling(ctx)

    def _emit_throttling(self, ctx: ContextProtocol) -> None:
        flags = self._read_throttled_flags()
        if flags is None:
            return

        ctx.events.emit(
            "system.throttling.updated",
            **flags,
        )

    def _read_throttled_flags(self) -> dict[str, bool | int] | None:
        path = Path("/sys/devices/platform/soc/soc:firmware/get_throttled")

        try:
            raw = path.read_text().strip()
            value = int(raw, 0)  # handles hex automatically
        except Exception:
            return None

        def bit(n: int) -> bool:
            return bool(value & (1 << n))

        return {
            # current state
            "undervoltage": bit(0),
            "freq_capped": bit(1),
            "throttled": bit(2),
            "soft_temp_limit": bit(3),
            # historical since boot
            "undervoltage_occurred": bit(16),
            "freq_capped_occurred": bit(17),
            "throttled_occurred": bit(18),
            "soft_temp_limit_occurred": bit(19),
            "raw": value,
        }
