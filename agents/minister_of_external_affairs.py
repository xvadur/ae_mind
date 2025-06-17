class MinisterOfExternalAffairs:
    def __init__(self, memory, constitution):
        self.name = "Minister of External Affairs"
        self.memory = memory
        self.constitution = constitution
    def activate(self):
        print(f"{self.name} aktivovaný.")
