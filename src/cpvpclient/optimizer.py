from __future__ import annotations

from dataclasses import dataclass

from .packets import OutgoingPacket, PacketType, Priority
from .scheduler import PacketScheduler
from .timing import TickTracker


@dataclass(slots=True)
class Vec3:
    x: float
    y: float
    z: float


def predict_position(current: Vec3, velocity_per_tick: Vec3, ticks: int = 2) -> Vec3:
    return Vec3(
        x=current.x + velocity_per_tick.x * ticks,
        y=current.y + velocity_per_tick.y * ticks,
        z=current.z + velocity_per_tick.z * ticks,
    )


class CrystalOptimizer:
    def __init__(self, tracker: TickTracker, scheduler: PacketScheduler) -> None:
        self.tracker = tracker
        self.scheduler = scheduler

    def schedule_place_and_break(
        self,
        now_ms: float,
        block_pos: tuple[int, int, int],
        enemy_pos: Vec3,
        enemy_velocity: Vec3,
    ) -> None:
        boundary = self.tracker.predicted_tick_boundary_ms(now_ms)
        place_at = max(now_ms, boundary - 2.0)
        break_at = boundary + 1.0

        predicted_enemy = predict_position(enemy_pos, enemy_velocity, ticks=2)

        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.ROTATION,
                payload={"look_at": (predicted_enemy.x, predicted_enemy.y, predicted_enemy.z)},
                priority=Priority.HIGH,
            ),
            send_at_ms=place_at - 0.5,
        )
        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.CRYSTAL_PLACE,
                payload={"block_pos": block_pos},
                priority=Priority.NORMAL,
            ),
            send_at_ms=place_at,
        )
        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.ATTACK_ENTITY,
                payload={"target": "new_crystal"},
                priority=Priority.NORMAL,
            ),
            send_at_ms=break_at,
        )


class AnchorOptimizer:
    def __init__(self, tracker: TickTracker, scheduler: PacketScheduler) -> None:
        self.tracker = tracker
        self.scheduler = scheduler

    def schedule_charge_and_detonate(
        self,
        now_ms: float,
        anchor_pos: tuple[int, int, int],
        look_at: Vec3,
    ) -> None:
        boundary = self.tracker.predicted_tick_boundary_ms(now_ms)
        charge_at = max(now_ms, boundary - 1.5)
        detonate_at = boundary + 0.8

        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.ROTATION,
                payload={"look_at": (look_at.x, look_at.y, look_at.z)},
                priority=Priority.HIGH,
            ),
            send_at_ms=charge_at - 0.4,
        )
        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.ANCHOR_CHARGE,
                payload={"anchor_pos": anchor_pos},
                priority=Priority.NORMAL,
            ),
            send_at_ms=charge_at,
        )
        self.scheduler.schedule(
            OutgoingPacket(
                packet_type=PacketType.ANCHOR_DETONATE,
                payload={"anchor_pos": anchor_pos},
                priority=Priority.NORMAL,
            ),
            send_at_ms=detonate_at,
        )
