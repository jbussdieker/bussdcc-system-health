from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class DeviceSpec:
    type: str
    config: dict[str, Any]


DeviceMap = dict[str, DeviceSpec]


def replace_devices(devices: DeviceMap) -> DeviceMap:
    return dict(devices)


def add_device(
    devices: DeviceMap,
    device: str,
    spec: DeviceSpec,
) -> DeviceMap:
    return {
        **devices,
        device: spec,
    }


def update_device_config(
    devices: DeviceMap,
    device: str,
    config: dict[str, object],
) -> DeviceMap:
    spec = devices[device]

    return {
        **devices,
        device: DeviceSpec(
            type=spec.type,
            config=config,
        ),
    }


def delete_device(
    devices: DeviceMap,
    device: str,
) -> DeviceMap:
    return {
        device_id: spec for device_id, spec in devices.items() if device_id != device
    }
