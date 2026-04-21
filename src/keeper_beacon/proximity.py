"""Proximity scorer — score agents by network latency, capability overlap, and trust."""
import time
from .registry import AgentRecord


class ProximityScorer:
    """Score how 'close' an agent is to a task or another agent."""

    def __init__(self, latency_weight: float = 0.3,
                 overlap_weight: float = 0.4,
                 trust_weight: float = 0.3):
        self._latency_w = latency_weight
        self._overlap_w = overlap_weight
        self._trust_w = trust_weight

    def score_for_task(self, agent: AgentRecord,
                       required_capabilities: list[str],
                       max_latency_ms: float = 100.0) -> float:
        """Score an agent's proximity to a task."""
        # Capability overlap (0-1)
        if required_capabilities:
            overlap = sum(1 for c in required_capabilities
                         if c in agent.capabilities) / len(required_capabilities)
        else:
            overlap = 1.0

        # Latency estimate (inverse of staleness as proxy)
        staleness = agent.staleness_seconds
        latency_score = max(0.0, 1.0 - (staleness / 300.0))

        # Trust
        trust = agent.trust_score

        return (overlap * self._overlap_w +
                latency_score * self._latency_w +
                trust * self._trust_w)

    def score_agents(self, agents: list[AgentRecord],
                     required_capabilities: list[str],
                     max_latency_ms: float = 100.0) -> list[tuple[AgentRecord, float]]:
        """Score and rank multiple agents."""
        scored = [(a, self.score_for_task(a, required_capabilities, max_latency_ms))
                  for a in agents]
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def find_cluster(self, agents: list[AgentRecord],
                     capability: str) -> list[AgentRecord]:
        """Find all agents with a specific capability."""
        return [a for a in agents if capability in a.capabilities]
