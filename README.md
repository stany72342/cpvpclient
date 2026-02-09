# cpvpclient

A client-side PvP optimizer focused on tick-aligned crystal and anchor interactions.

## Goal
Provide a timing and packet-control layer that improves the consistency of manual PvP actions without automating gameplay. You still aim and click; the client aligns packet timing and ordering so the server processes your actions on the earliest possible tick.

## Core Concepts
- **Tick alignment**: Server ticks run at 20 TPS (50 ms). The client schedules packets to land just before tick boundaries so actions are processed on the current tick instead of the next one.
- **Position prediction**: Short-horizon prediction (1–2 ticks) helps pre-rotate and validate interactions against expected entity positions.
- **Packet ordering**: Outgoing packets are ordered to match server expectations for consistent placement and detonation.

## Implemented Modules
### TickTracker
Tracks the server tick cadence using movement confirmations and latency samples.

### PacketScheduler
Queues outgoing packets and decides whether to send immediately or delay for same-tick processing.

### CrystalOptimizer
Schedules server-rotation, crystal placement, and break packets across the closest tick boundary.

### AnchorOptimizer
Schedules charge and detonate packets across a tick boundary with explicit rotation ordering.

## Non-Goals
- No automated aiming or target selection
- No automated clicks or action macros
- No server-side exploits

## Install
```bash
python -m pip install -e .
```

## Run Tests
```bash
python -m pytest -q
```

## High-Level Flow
```
Input
  -> Optimizer (TickTracker + PacketScheduler)
    -> Protocol Pipeline
      -> Server
```

## Notes
This repository currently provides a standalone optimizer core (timing, scheduling, and packet plans). Integrating it into a full Minecraft protocol pipeline is the next step.
