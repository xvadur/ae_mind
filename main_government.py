from agents.premier import Premier
from ministers.memory import MinisterOfMemory, AssistantOfMemory
from ministers.communication import (
    MinisterOfCommunication,
    AssistantOfCommunication,
)
from ministers.coordination import (
    MinisterOfCoordination,
    AssistantOfCoordination,
)
from ministers.development import (
    MinisterOfDevelopment,
    AssistantOfDevelopment,
)
from ministers.interface import MinisterOfInterface, AssistantOfInterface
from ministers.external_affairs import (
    MinisterOfExternalAffairs,
    AssistantOfExternalAffairs,
)
from memory.shared_memory import SharedMemory
import yaml
import os
import sys

def load_constitution(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def initialize_government():
    # 1. Načítaj ústavu
    constitution_path = os.path.join("constitution", "constitution_monumentum_veritas.yaml")
    constitution = load_constitution(constitution_path)
    # 2. Inicializuj zdieľanú pamäť
    shared_memory = SharedMemory()
    shared_memory.load()
    # 3. Inicializuj ministrov a asistentov
    ministers = [
        (MinisterOfMemory(shared_memory), AssistantOfMemory(shared_memory)),
        (MinisterOfCommunication(shared_memory), AssistantOfCommunication(shared_memory)),
        (MinisterOfCoordination(shared_memory), AssistantOfCoordination(shared_memory)),
        (MinisterOfDevelopment(shared_memory), AssistantOfDevelopment(shared_memory)),
        (MinisterOfInterface(shared_memory), AssistantOfInterface(shared_memory)),
        (MinisterOfExternalAffairs(shared_memory), AssistantOfExternalAffairs(shared_memory)),
    ]
    premier = Premier(ministers, shared_memory, constitution)
    premier.run_government()
    return premier, ministers, shared_memory


if __name__ == "__main__":
    premier, ministers, shared_memory = initialize_government()

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "run":
            cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            premier.main_loop(cycles=cycles)
        elif cmd == "status":
            premier.show_status()
        elif cmd == "queue":
            premier.show_queue()
        else:
            print("Unknown command")
    else:
        tasks = ["Test task 1", "Test task 2", "Test task 3"]
        for idx, (minister, _) in enumerate(ministers):
            task = tasks[idx % len(tasks)]
            premier.send_task(minister.__class__.__name__, task)

        for minister, _ in ministers:
            result = minister.introspect()
            shared_memory.write_log({
                "type": "INTROSPECT",
                "minister": minister.__class__.__name__,
                "output": result,
            })

        premier.run_reflection_cycle()
        premier.generate_adaptive_directives()

