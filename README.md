# BussDCC System Health

**bussdcc-system-health** is a reference application demonstrating how to build a real system using **bussdcc** — a deterministic cybernetic runtime for Python.

It monitors host system health and exposes:

* live metrics via a web dashboard
* structured event streams
* historical JSONL logging
* real-time UI updates through WebSockets

The project is intentionally small but complete. It shows how **services, processes, interfaces, and sinks** work together inside a bussdcc runtime.

## Overview

This application collects and visualizes system telemetry:

* CPU usage
* Memory usage
* Disk usage
* System load averages
* CPU temperature
* Network throughput
* Hardware throttling / undervoltage status (Raspberry Pi compatible)
* Host identity information

The runtime emits events continuously, which are:

1. processed into state
2. streamed to a web interface
3. logged to disk

This demonstrates bussdcc’s core pattern:

```
Service → Events → Process → State → Interface → UI
             ↓
           Sinks
```

## Architecture

The project intentionally mirrors bussdcc’s runtime model.

### Services

**`SystemService`**

Runs periodically and emits system telemetry events:

```
system.memory.usage.updated
system.cpu.usage.updated
system.disk.usage.updated
system.temperature.updated
system.network.usage.updated
system.throttling.updated
```

Services are responsible only for **observing the world** and emitting events.

### Processes

**`SystemProcess`**

Consumes events and updates runtime state:

```python
ctx.state.set("system.cpu.usage", evt.data)
```

Processes transform event streams into structured shared state.

### Interface

**`SystemWebInterface`**

* Runs a Flask + Socket.IO server
* Streams runtime events to the browser
* Renders state snapshots on page load

Interfaces expose the system externally without coupling to services.

### Event Sinks

Two sinks demonstrate observability patterns:

#### ConsoleSink

Prints structured JSON events to stdout.

#### JsonlSink

Writes rotating JSONL event logs:

```
data/history/YYYY-MM-DD/HH-MM-SS.jsonl
```

Each line is a single immutable event record.

## Dashboard

The web UI provides live system visibility:

* ✅ Health status indicator
* CPU usage breakdown
* Memory & disk utilization
* Load averages
* Network throughput per interface
* Thermal & power throttling detection

Updates occur in real time using Socket.IO events emitted directly from the runtime.

## Installation

Requires Python 3.11+.

```bash
pip install bussdcc-system-health
```

Or install locally:

```bash
pip install -e .
```

## Running

Start the runtime:

```bash
bussdcc-system-health
```

Then open:

```
http://localhost:8086
```

## Example Event Output

Console sink output:

```json
{"time":"2026-01-01T12:00:00Z","name":"system.cpu.usage.updated","data":{"user":12.4,"system":3.1,"idle":84.5}}
```

This illustrates bussdcc’s core idea:

> the system is an event stream first, UI second.

## Project Structure

```
bussdcc_system_health/
├── cli.py            # runtime entrypoint
├── runtime/          # custom runtime lifecycle
├── services/         # telemetry collection
├── processes/        # state projection
├── interfaces/       # web UI
└── sinks/            # event logging
```

## What This Example Demonstrates

This project is designed as a learning reference for bussdcc concepts:

| Concept               | Demonstrated By  |
| --------------------- | ---------------- |
| Deterministic runtime | custom Runtime   |
| Periodic services     | SystemService    |
| Event-driven state    | SystemProcess    |
| External interfaces   | Flask web UI     |
| Observability         | sinks            |
| Real-time updates     | Socket.IO bridge |

## Why bussdcc?

Traditional applications couple:

```
logic ↔ UI ↔ IO ↔ background work
```

bussdcc separates responsibilities through events:

```
observe → emit → transform → expose
```

This leads to systems that are:

* easier to reason about
* deterministic
* observable by default
* naturally extensible

## Hardware Notes

Some features depend on Linux system interfaces:

| Feature              | Platform                 |
| -------------------- | ------------------------ |
| CPU temperature      | Linux SBC / Raspberry Pi |
| Throttling detection | Raspberry Pi firmware    |
| Network metrics      | Linux                    |

The application still runs on non-Pi systems, but certain fields may be unavailable.

## Development

Install dependencies:

```bash
pip install -e .[dev]
```

Run directly:

```bash
python -m bussdcc_system_health.cli
```

## License

MIT License

## Related

* bussdcc runtime: [https://github.com/jbussdieker/bussdcc](https://github.com/jbussdieker/bussdcc)
