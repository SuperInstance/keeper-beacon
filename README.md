# keeper-beacon

[![PyPI](https://img.shields.io/pypi/v/keeper-beacon)](https://pypi.org/project/keeper-beacon/) [![Python](https://img.shields.io/pypi/pyversions/keeper-beacon)](https://pypi.org/project/keeper-beacon/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Fleet discovery and registry — agents appear on radar, get tracked and routed.

The lighthouse keeper needs to know where every agent is. Keeper Beacon provides fleet discovery, registration, and proximity tracking.

## What It Does

- **Discovery** — Agents register with the beacon on startup
- **Registry** — Central directory of active fleet members
- **Proximity** — Track which agents are near each other (same task, same room)
- **Matcher** — Route agents to tasks based on capabilities and proximity

## The Lighthouse Metaphor

The Cocapn brand IS the architecture. The lighthouse (keeper) monitors agent proximity. Radar rings represent fleet discovery. Each ring is an agent appearing on the radar, being tracked, authenticated, and routed.

## Installation

```bash
pip install keeper-beacon
```

## Part of the Cocapn Fleet

Powers the Keeper service on port 8900.

## License

MIT