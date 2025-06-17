class MinisterOfMemory:
    def __init__(self, memory, constitution):
        self.name = "Minister of Memory"
        self.memory = memory
        self.constitution = constitution
    def activate(self):
        print(f"{self.name} aktivovaný.")
