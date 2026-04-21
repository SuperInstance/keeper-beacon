"""Tests for keeper-beacon."""
import time
import pytest
from keeper_beacon import (
    AgentRegistry, AgentRecord, AgentStatus,
    BeaconDiscovery, BeaconSignal,
    CapabilityMatcher, MatchResult, ProximityScorer,
)


class TestAgentRecord:
    def test_create(self):
        rec = AgentRecord(agent_id="oracle1", name="Oracle1",
                          capabilities=["reading", "synthesis"], endpoint="keeper:8900")
        assert rec.is_available
        assert rec.trust_score == 0.5

    def test_load_affects_availability(self):
        rec = AgentRecord(agent_id="busy", name="BusyAgent", load=0.95)
        assert not rec.is_available


class TestRegistry:
    def test_register_and_get(self):
        reg = AgentRegistry()
        rec = AgentRecord(agent_id="a1", name="Agent1")
        assert reg.register(rec)
        assert not reg.register(rec)  # update, not new
        assert reg.get("a1").name == "Agent1"
        assert reg.size == 1

    def test_heartbeat(self):
        reg = AgentRegistry()
        rec = AgentRecord(agent_id="a1", name="Agent1", last_seen=time.time() - 100)
        reg.register(rec)
        old = reg.get("a1").last_seen
        reg.heartbeat("a1")
        assert reg.get("a1").last_seen > old

    def test_stale_agents_offline(self):
        reg = AgentRegistry(stale_threshold=1.0)
        rec = AgentRecord(agent_id="a1", name="Agent1",
                          last_seen=time.time() - 5)
        reg.register(rec)
        active = reg.active_agents
        assert len(active) == 0

    def test_stats(self):
        reg = AgentRegistry(stale_threshold=999)
        reg.register(AgentRecord(agent_id="a1", name="A1", status=AgentStatus.ACTIVE))
        reg.register(AgentRecord(agent_id="a2", name="A2", status=AgentStatus.IDLE))
        stats = reg.stats()
        assert stats["total"] == 2


class TestBeaconDiscovery:
    def test_receive_and_discover(self):
        disc = BeaconDiscovery()
        disc.receive(BeaconSignal(agent_id="a1", name="Agent1", capabilities=["coding"]))
        disc.receive(BeaconSignal(agent_id="a2", name="Agent2", capabilities=["vision"]))
        found = disc.discover(capability="coding")
        assert len(found) == 1
        assert found[0].agent_id == "a1"

    def test_expired(self):
        disc = BeaconDiscovery()
        disc.receive(BeaconSignal(agent_id="old", name="Old", timestamp=time.time() - 200, ttl=60))
        assert disc.active_count == 0

    def test_prune(self):
        disc = BeaconDiscovery()
        disc.receive(BeaconSignal(agent_id="old", name="Old", timestamp=time.time() - 200, ttl=60))
        disc.receive(BeaconSignal(agent_id="new", name="New", timestamp=time.time(), ttl=60))
        removed = disc.prune()
        assert removed == 1
        assert disc.total_count == 1


class TestCapabilityMatcher:
    def test_match(self):
        agents = [
            AgentRecord(agent_id="a1", name="Coder",
                        capabilities=["python", "rust"], trust_score=0.8, load=0.2),
            AgentRecord(agent_id="a2", name="Writer",
                        capabilities=["docs"], trust_score=0.5, load=0.1),
        ]
        matcher = CapabilityMatcher()
        results = matcher.match(agents, ["python", "rust"])
        assert len(results) == 2
        assert results[0].agent.agent_id == "a1"
        assert results[0].is_fully_capable
        assert not results[1].is_fully_capable

    def test_fully_capable(self):
        agents = [
            AgentRecord(agent_id="a1", name="Full", capabilities=["a", "b", "c"]),
            AgentRecord(agent_id="a2", name="Partial", capabilities=["a"]),
        ]
        matcher = CapabilityMatcher()
        results = matcher.fully_capable(agents, ["a", "b"])
        assert len(results) == 1
        assert results[0].agent.agent_id == "a1"


class TestProximityScorer:
    def test_score(self):
        agent = AgentRecord(agent_id="a1", name="Near",
                            capabilities=["python"], trust_score=0.9,
                            last_seen=time.time())
        scorer = ProximityScorer()
        score = scorer.score_for_task(agent, ["python"])
        assert score > 0.5

    def test_rank(self):
        agents = [
            AgentRecord(agent_id="good", name="Good",
                        capabilities=["python"], trust_score=0.9, load=0.1),
            AgentRecord(agent_id="ok", name="OK",
                        capabilities=["python"], trust_score=0.5, load=0.5),
        ]
        scorer = ProximityScorer()
        ranked = scorer.score_agents(agents, ["python"])
        assert ranked[0][0].agent_id == "good"

    def test_cluster(self):
        agents = [
            AgentRecord(agent_id="a1", name="A1", capabilities=["cuda", "training"]),
            AgentRecord(agent_id="a2", name="A2", capabilities=["docs"]),
        ]
        scorer = ProximityScorer()
        cluster = scorer.find_cluster(agents, "cuda")
        assert len(cluster) == 1
