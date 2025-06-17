class AssistantOfMemory:
    def __init__(self, memory):
        self.name = "Assistant of Memory"
        self.memory = memory
    def activate(self):
        print(f"{self.name} aktivovaný.")
