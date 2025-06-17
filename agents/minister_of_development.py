class MinisterOfDevelopment:
    def __init__(self, memory, constitution):
        self.name = "Minister of Development"
        self.memory = memory
        self.constitution = constitution
    def activate(self):
        print(f"{self.name} aktivovaný.")
