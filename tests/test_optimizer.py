from cpvpclient import (
    AnchorOptimizer,
    CrystalOptimizer,
    PacketScheduler,
    PacketType,
    TickTracker,
    Vec3,
)


def test_tick_tracker_next_tick():
    tracker = TickTracker(tick_ms=50)
    tracker.initialize(1000)
    assert tracker.next_tick_in_ms(1023) == 27


def test_crystal_ordering():
    tracker = TickTracker(tick_ms=50)
    tracker.initialize(1000)
    scheduler = PacketScheduler()
    opt = CrystalOptimizer(tracker, scheduler)

    opt.schedule_place_and_break(
        now_ms=1023,
        block_pos=(10, 64, 10),
        enemy_pos=Vec3(12, 64, 12),
        enemy_velocity=Vec3(0.1, 0, 0.0),
    )

    packets = scheduler.ready_packets(1055)
    assert [p.packet_type for p in packets] == [
        PacketType.ROTATION,
        PacketType.CRYSTAL_PLACE,
        PacketType.ATTACK_ENTITY,
    ]


def test_anchor_charge_before_detonate():
    tracker = TickTracker(tick_ms=50)
    tracker.initialize(1000)
    scheduler = PacketScheduler()
    opt = AnchorOptimizer(tracker, scheduler)

    opt.schedule_charge_and_detonate(
        now_ms=1023,
        anchor_pos=(8, 64, 8),
        look_at=Vec3(8.5, 64.5, 8.5),
    )

    packets = scheduler.ready_packets(1055)
    assert [p.packet_type for p in packets] == [
        PacketType.ROTATION,
        PacketType.ANCHOR_CHARGE,
        PacketType.ANCHOR_DETONATE,
    ]
