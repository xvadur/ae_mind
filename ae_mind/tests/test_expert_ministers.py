import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from memory.shared_memory import SharedMemory
from ministers.emergent_synthesis import MinisterOfEmergentSynthesis
from ministers.quantum_resilience import MinisterOfQuantumResilience
from ministers.ethical_topology import MinisterOfEthicalTopology
from ministers.dynamic_foresight import MinisterOfDynamicForesight
from ministers.narrative_weaving import MinisterOfNarrativeWeaving


def test_expert_ministers_basic():
    memory = SharedMemory()
    ministers = [
        MinisterOfEmergentSynthesis(memory),
        MinisterOfQuantumResilience(memory),
        MinisterOfEthicalTopology(memory),
        MinisterOfDynamicForesight(memory),
        MinisterOfNarrativeWeaving(memory),
    ]
    for minister in ministers:
        minister.activate()
        result = minister.process_request("task one; task two")
        assert isinstance(result, str)
        introspect = minister.introspect()
        assert isinstance(introspect, dict)
