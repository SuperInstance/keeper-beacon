"""Beacon discovery — broadcast and receive agent presence signals."""
import hashlib
import time
from dataclasses import dataclass, field


@dataclass
class BeaconSignal:
    """A beacon broadcast from an agent."""
    agent_id: str
    name: str
    capabilities: list[str] = field(default_factory=list)
    endpoint: str = ""
    timestamp: float = 0.0
    ttl: float = 60.0  # time-to-live in seconds
    signature: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()
        if not self.signature:
            self.signature = self._compute_signature()

    def _compute_signature(self) -> str:
        content = f"{self.agent_id}:{self.name}:{self.endpoint}:{self.timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.timestamp) > self.ttl

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id, "name": self.name,
            "capabilities": self.capabilities, "endpoint": self.endpoint,
            "timestamp": self.timestamp, "ttl": self.ttl,
            "expired": self.is_expired,
        }


class BeaconDiscovery:
    """Receive and process beacon signals from fleet agents."""

    def __init__(self, ttl: float = 120.0):
        self._signals: dict[str, BeaconSignal] = {}
        self._ttl = ttl

    def receive(self, signal: BeaconSignal) -> bool:
        """Receive a beacon signal. Returns True if new or updated."""
        is_new = signal.agent_id not in self._signals
        self._signals[signal.agent_id] = signal
        return is_new

    def discover(self, capability: str | None = None) -> list[BeaconSignal]:
        """Find active signals, optionally filtered by capability."""
        results = []
        for sig in self._signals.values():
            if sig.is_expired:
                continue
            if capability and capability not in sig.capabilities:
                continue
            results.append(sig)
        return sorted(results, key=lambda s: s.timestamp, reverse=True)

    def prune(self) -> int:
        """Remove expired signals. Returns count removed."""
        expired = [aid for aid, sig in self._signals.items() if sig.is_expired]
        for aid in expired:
            del self._signals[aid]
        return len(expired)

    @property
    def active_count(self) -> int:
        return sum(1 for s in self._signals.values() if not s.is_expired)

    @property
    def total_count(self) -> int:
        return len(self._signals)
