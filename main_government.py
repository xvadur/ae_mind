from agents.premier import Premier
from agents.minister_of_memory import MinisterOfMemory
from agents.assistant_of_memory import AssistantOfMemory
from agents.minister_of_communication import MinisterOfCommunication
from agents.assistant_of_communication import AssistantOfCommunication
from agents.minister_of_coordination import MinisterOfCoordination
from agents.assistant_of_coordination import AssistantOfCoordination
from agents.minister_of_development import MinisterOfDevelopment
from agents.assistant_of_development import AssistantOfDevelopment
from agents.minister_of_interface import MinisterOfInterface
from agents.assistant_of_interface import AssistantOfInterface
from agents.minister_of_external_affairs import MinisterOfExternalAffairs
from agents.assistant_of_external_affairs import AssistantOfExternalAffairs
from memory.shared_memory import SharedMemory
import yaml
import os

def load_constitution(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    # 1. Načítaj ústavu
    constitution_path = os.path.join("constitution", "constitution_monumentum_veritas.yaml")
    constitution = load_constitution(constitution_path)
    # 2. Inicializuj zdieľanú pamäť
    shared_memory = SharedMemory()
    shared_memory.load()
    # 3. Inicializuj ministrov a asistentov
    ministers = [
        (MinisterOfMemory(shared_memory, constitution), AssistantOfMemory(shared_memory)),
        (MinisterOfCommunication(shared_memory, constitution), AssistantOfCommunication(shared_memory)),
        (MinisterOfCoordination(shared_memory, constitution), AssistantOfCoordination(shared_memory)),
        (MinisterOfDevelopment(shared_memory, constitution), AssistantOfDevelopment(shared_memory)),
        (MinisterOfInterface(shared_memory, constitution), AssistantOfInterface(shared_memory)),
        (MinisterOfExternalAffairs(shared_memory, constitution), AssistantOfExternalAffairs(shared_memory)),
    ]
    # 4. Inicializuj Premiera
    premier = Premier(ministers, shared_memory, constitution)
    # 5. Spusti vládu
    premier.run_government()
