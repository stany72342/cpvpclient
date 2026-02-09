# cpvpclient

A client-side PvP optimizer focused on tick-aligned crystal and anchor interactions.

## Goal
Provide a timing and packet-control layer that improves the consistency of manual PvP actions without automating gameplay. You still aim and click; the client aligns packet timing and ordering so the server processes your actions on the earliest possible tick.

## Core Concepts
- **Tick alignment**: Server ticks run at 20 TPS (50 ms). The client schedules packets to land just before tick boundaries so actions are processed on the current tick instead of the next one.
- **Position prediction**: Short-horizon prediction (1–2 ticks) helps pre-rotate and validate interactions against expected entity positions.
- **Packet ordering**: Outgoing packets are ordered to match server expectations for consistent placement and detonation.

## Modules
### TickTracker
Tracks the server tick cadence using movement confirmations and latency samples. Exposes timing primitives like:
- `nextTickInMs()`
- `timeSinceLastTickMs()`

### PacketScheduler
Queues outgoing packets and decides whether to send immediately or delay for same-tick processing. Supports:
- exact millisecond scheduling
- packet priority (e.g., rotation before use)
- ordering constraints

### CrystalOptimizer
Intercepts crystal placement and attack actions.

Responsibilities:
- Pre-rotation adjustment before placement
- Schedules placement packets just before tick boundary
- Queues attack packets on the spawn tick for instant pop

### AnchorOptimizer
Handles respawn anchor charge and detonation timing.

Responsibilities:
- Charge packet at end of tick
- Detonation at start of next tick
- Server-side face validation via rotation ordering

## Non-Goals
- No automated aiming or target selection
- No automated clicks or action macros
- No server-side exploits

## High-Level Flow
```
Input
  -> Optimizer (TickTracker + PacketScheduler)
    -> Protocol Pipeline
      -> Server
```

## Example Timing
- Click at 23 ms into tick
- Scheduler waits 25 ms
- Packet lands at 48–49 ms
- Server processes on current tick

## Status
This repository currently contains the architectural spec and high-level design. Implementation details will be added in future revisions.
