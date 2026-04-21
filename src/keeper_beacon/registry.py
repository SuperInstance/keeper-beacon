"""Agent registry — track fleet members and their status."""
import time
from dataclasses import dataclass, field
from enum import Enum


class AgentStatus(Enum):
    ACTIVE = "active"
    IDLE = "idle"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


@dataclass
class AgentRecord:
    agent_id: str
    name: str
    capabilities: list[str] = field(default_factory=list)
    endpoint: str = ""
    status: AgentStatus = AgentStatus.ACTIVE
    last_seen: float = 0.0
    metadata: dict = field(default_factory=dict)
    trust_score: float = 0.5
    load: float = 0.0  # 0.0-1.0 current workload

    def __post_init__(self):
        if not self.last_seen:
            self.last_seen = time.time()

    @property
    def is_available(self) -> bool:
        return self.status == AgentStatus.ACTIVE and self.load < 0.9

    @property
    def staleness_seconds(self) -> float:
        return time.time() - self.last_seen

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id, "name": self.name,
            "capabilities": self.capabilities, "endpoint": self.endpoint,
            "status": self.status.value, "trust_score": self.trust_score,
            "load": self.load, "last_seen": self.last_seen,
        }


class AgentRegistry:
    """Registry of fleet agents with health tracking."""

    def __init__(self, stale_threshold: float = 300.0):
        self._agents: dict[str, AgentRecord] = {}
        self._stale_threshold = stale_threshold

    def register(self, record: AgentRecord) -> bool:
        """Register or update an agent. Returns True if new."""
        is_new = record.agent_id not in self._agents
        self._agents[record.agent_id] = record
        return is_new

    def deregister(self, agent_id: str) -> bool:
        return self._agents.pop(agent_id, None) is not None

    def get(self, agent_id: str) -> AgentRecord | None:
        return self._agents.get(agent_id)

    def heartbeat(self, agent_id: str) -> bool:
        """Update last_seen for an agent."""
        rec = self._agents.get(agent_id)
        if rec:
            rec.last_seen = time.time()
            return True
        return False

    @property
    def active_agents(self) -> list[AgentRecord]:
        self._mark_stale()
        return [a for a in self._agents.values() if a.status == AgentStatus.ACTIVE]

    @property
    def all_agents(self) -> list[AgentRecord]:
        return list(self._agents.values())

    @property
    def size(self) -> int:
        return len(self._agents)

    def _mark_stale(self):
        """Mark stale agents as offline."""
        now = time.time()
        for agent in self._agents.values():
            if agent.status == AgentStatus.ACTIVE and (now - agent.last_seen) > self._stale_threshold:
                agent.status = AgentStatus.OFFLINE

    def stats(self) -> dict:
        self._mark_stale()
        counts = {}
        for a in self._agents.values():
            counts[a.status.value] = counts.get(a.status.value, 0) + 1
        return {"total": self.size, "by_status": counts}
