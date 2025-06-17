class MinisterOfCoordination:
    def __init__(self, memory, constitution):
        self.name = "Minister of Coordination"
        self.memory = memory
        self.constitution = constitution
    def activate(self):
        print(f"{self.name} aktivovaný.")
