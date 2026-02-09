from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import List

from .packets import OutgoingPacket


@dataclass(order=True, slots=True)
class ScheduledPacket:
    send_at_ms: float
    priority_rank: int
    sequence: int
    packet: OutgoingPacket = field(compare=False)


class PacketScheduler:
    """Millisecond-level packet scheduler with ordering guarantees."""

    def __init__(self) -> None:
        self._queue: List[ScheduledPacket] = []
        self._sequence = 0

    def schedule(self, packet: OutgoingPacket, send_at_ms: float) -> None:
        heapq.heappush(
            self._queue,
            ScheduledPacket(
                send_at_ms=send_at_ms,
                priority_rank=packet.priority.value,
                sequence=self._sequence,
                packet=packet,
            ),
        )
        self._sequence += 1

    def ready_packets(self, now_ms: float) -> list[OutgoingPacket]:
        ready: list[OutgoingPacket] = []
        while self._queue and self._queue[0].send_at_ms <= now_ms:
            ready.append(heapq.heappop(self._queue).packet)
        return ready

    def queued_count(self) -> int:
        return len(self._queue)
