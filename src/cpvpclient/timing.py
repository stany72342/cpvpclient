from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TickTracker:
    """Tracks a rolling estimate of server tick boundaries.

    The tracker models 20 TPS by default (50 ms tick duration) and can be
    updated from observed server confirmations.
    """

    tick_ms: float = 50.0
    smoothing: float = 0.2
    _last_tick_time_ms: float = 0.0
    _latency_ms: float = 0.0

    def initialize(self, now_ms: float) -> None:
        self._last_tick_time_ms = now_ms

    def observe_tick(self, now_ms: float) -> None:
        """Update last known tick timestamp from an observed server event."""
        if self._last_tick_time_ms == 0.0:
            self._last_tick_time_ms = now_ms
            return
        observed = now_ms - self._last_tick_time_ms
        self.tick_ms = (1 - self.smoothing) * self.tick_ms + self.smoothing * observed
        self._last_tick_time_ms = now_ms

    def set_latency(self, rtt_ms: float) -> None:
        self._latency_ms = max(0.0, rtt_ms / 2.0)

    @property
    def one_way_latency_ms(self) -> float:
        return self._latency_ms

    def time_since_last_tick_ms(self, now_ms: float) -> float:
        return max(0.0, now_ms - self._last_tick_time_ms)

    def next_tick_in_ms(self, now_ms: float) -> float:
        elapsed = self.time_since_last_tick_ms(now_ms)
        remainder = self.tick_ms - (elapsed % self.tick_ms)
        return 0.0 if abs(remainder - self.tick_ms) < 1e-6 else remainder

    def predicted_tick_boundary_ms(self, now_ms: float, ticks_ahead: int = 0) -> float:
        return now_ms + self.next_tick_in_ms(now_ms) + ticks_ahead * self.tick_ms
