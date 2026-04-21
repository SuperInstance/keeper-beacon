"""Capability matcher — find best agents for tasks based on capabilities and load."""
from dataclasses import dataclass
from .registry import AgentRecord


@dataclass
class MatchResult:
    agent: AgentRecord
    score: float  # 0.0-1.0
    matched_capabilities: list[str]
    missing_capabilities: list[str]

    @property
    def is_fully_capable(self) -> bool:
        return len(self.missing_capabilities) == 0

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent.agent_id, "name": self.agent.name,
            "score": round(self.score, 3),
            "matched": self.matched_capabilities,
            "missing": self.missing_capabilities,
            "fully_capable": self.is_fully_capable,
        }


class CapabilityMatcher:
    """Match tasks to agents based on required capabilities."""

    def __init__(self, trust_weight: float = 0.3, load_weight: float = 0.2,
                 capability_weight: float = 0.5):
        self._tw = trust_weight
        self._lw = load_weight
        self._cw = capability_weight

    def match(self, agents: list[AgentRecord],
              required: list[str]) -> list[MatchResult]:
        """Find and rank agents for a set of required capabilities."""
        results = []
        for agent in agents:
            matched = [c for c in required if c in agent.capabilities]
            missing = [c for c in required if c not in agent.capabilities]

            cap_score = len(matched) / len(required) if required else 1.0
            load_score = 1.0 - agent.load
            trust_score = agent.trust_score

            score = (cap_score * self._cw + load_score * self._lw +
                     trust_score * self._tw)

            results.append(MatchResult(
                agent=agent, score=score,
                matched_capabilities=matched,
                missing_capabilities=missing,
            ))

        return sorted(results, key=lambda r: r.score, reverse=True)

    def best_match(self, agents: list[AgentRecord],
                   required: list[str]) -> MatchResult | None:
        matches = self.match(agents, required)
        return matches[0] if matches else None

    def fully_capable(self, agents: list[AgentRecord],
                      required: list[str]) -> list[MatchResult]:
        """Return only agents that have ALL required capabilities."""
        matches = self.match(agents, required)
        return [m for m in matches if m.is_fully_capable]
