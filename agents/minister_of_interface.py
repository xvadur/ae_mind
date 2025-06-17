class MinisterOfInterface:
    def __init__(self, memory, constitution):
        self.name = "Minister of Interface"
        self.memory = memory
        self.constitution = constitution
    def activate(self):
        print(f"{self.name} aktivovaný.")
