from dataclasses import dataclass

from bussdcc import Message

from ..model import DeviceSpec


@dataclass(slots=True, frozen=True)
class DevicesReplaced(Message):
    devices: dict[str, DeviceSpec]


@dataclass(slots=True, frozen=True)
class DeviceAdded(Message):
    device: str
    spec: DeviceSpec


@dataclass(slots=True, frozen=True)
class DeviceConfigUpdate(Message):
    device: str
    config: dict[str, object]


@dataclass(slots=True, frozen=True)
class DeviceDeleted(Message):
    device: str
