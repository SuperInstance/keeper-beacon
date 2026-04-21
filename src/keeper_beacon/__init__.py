"""Keeper Beacon — fleet discovery and registry."""
from .registry import AgentRegistry, AgentRecord, AgentStatus
from .discovery import BeaconDiscovery, BeaconSignal
from .matcher import CapabilityMatcher, MatchResult
from .proximity import ProximityScorer

__version__ = "0.1.0"
__all__ = [
    "AgentRegistry", "AgentRecord", "BeaconDiscovery", "BeaconSignal",
    "CapabilityMatcher", "MatchResult", "ProximityScorer",
]
