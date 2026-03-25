from bussdcc import ContextProtocol, Event, Message, Process

from .. import message
from ..model.device import (
    add_device,
    update_device_config,
    delete_device,
    replace_devices,
)


class DeviceManagerProcess(Process):
    name = "device_manager"

    def handle_event(self, ctx: ContextProtocol, evt: Event[Message]) -> None:
        payload = evt.payload

        if isinstance(payload, message.DevicesReplaced):
            ctx.state.set("devices", replace_devices(payload.devices))
            return

        if isinstance(payload, message.DeviceAdded):
            ctx.state.update(
                "devices",
                lambda devices: add_device(
                    devices or {},
                    payload.device,
                    payload.spec,
                ),
            )
            return

        if isinstance(payload, message.DeviceConfigUpdate):
            ctx.state.update(
                "devices",
                lambda devices: update_device_config(
                    devices or {},
                    payload.device,
                    payload.config,
                ),
            )
            return

        if isinstance(payload, message.DeviceDeleted):
            ctx.state.update(
                "devices",
                lambda devices: delete_device(
                    devices or {},
                    payload.device,
                ),
            )
