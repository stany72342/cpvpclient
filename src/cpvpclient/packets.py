from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class PacketType(Enum):
    ROTATION = auto()
    CRYSTAL_PLACE = auto()
    ATTACK_ENTITY = auto()
    ANCHOR_CHARGE = auto()
    ANCHOR_DETONATE = auto()


class Priority(Enum):
    HIGH = 0
    NORMAL = 1
    LOW = 2


@dataclass(slots=True)
class OutgoingPacket:
    packet_type: PacketType
    payload: dict[str, Any] = field(default_factory=dict)
    priority: Priority = Priority.NORMAL
