# cpvpclient

A standalone **PvP Optimizer Client** focused on precise timing and packet delivery for End Crystals and Respawn Anchors. You still aim and click—this client simply makes sure the server receives those actions at the mathematically optimal moment.

## What this client does

It inserts a thin optimization layer between your input and the Minecraft protocol:

```
Your input → Optimizer → Minecraft protocol → Server
```

That optimizer focuses on three jobs:

- **Tick alignment**: send packets at the ideal moment within the 50 ms server tick.
- **Position prediction**: estimate where entities will be when the server processes your action.
- **Packet ordering**: deliver packets in the sequence the server expects for same-tick outcomes.

This is **not automation**. It does not aim, click, or decide for you. It only optimizes delivery of what you already do.

## Core concept: server tick alignment

Minecraft servers run at 20 TPS (1 tick every 50 ms). If you place a crystal at a random time, you can lose a full tick to server scheduling. The optimizer delays or advances packet send time so your action lands on the current tick whenever possible.

## Crystal optimizer (client-side)

Optimizes only when you:

- Place a crystal
- Hit a crystal

Behavior:

- Predicts where the target will be in ~2 ticks.
- Adjusts your rotation packet before placing.
- Schedules **PLACE** just before the tick boundary.
- Queues **ATTACK** to land on the crystal’s spawn tick.

Result: faster pops, fewer late explosions, and better trade outcomes—without changing how you play.

## Anchor optimizer (client-side)

Respawn anchors are extremely timing-sensitive and often fail due to packet order and tick timing. The optimizer ensures:

- **Charge** packet lands at the end of the current tick.
- **Explode** packet lands at the start of the next tick.
- Rotation is valid on the server for a consistent interaction face.
- Dead-clicks and ghost anchors are prevented.

Result: anchors explode on the first possible tick every time.

## Module overview

```
PvPOptimizerClient
 ├── TickTracker
 ├── PacketScheduler
 ├── CrystalOptimizer
 └── AnchorOptimizer
```

### 1) TickTracker

Tracks exact server tick timing using movement confirmations and ping. Everything else uses this.

### 2) PacketScheduler

Queues outgoing packets and sends them at the optimal millisecond within the tick window.

### 3) CrystalOptimizer

Intercepts place/attack packets, adjusts timing and rotation ordering for same-tick place+break.

### 4) AnchorOptimizer

Coordinates charge/explode packets across the tick boundary for consistent detonations.

## Why a standalone client

A standalone client can control raw packet send time, Netty ordering, and outgoing queues with millisecond precision. This makes precise tick alignment possible in a way mods often cannot.

## In one sentence

**A Crystal + Anchor Optimizer Client is a timing and packet-control layer that aligns your PvP actions with server ticks so every crystal and anchor interaction happens on the first possible server tick.**
