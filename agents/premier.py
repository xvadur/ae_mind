class Premier:
    def __init__(self, council, shared_memory, constitution):
        self.name = "Premier Aethero_Xvadur"
        self.council = council
        self.shared_memory = shared_memory
        self.constitution = constitution
    def run_government(self):
        print(f"{self.name} inicializuje vládu podľa ústavy.")
        for minister, assistant in self.council:
            minister.activate()
            assistant.activate()
        print("Vláda AetheroOS je pripravená na výkon.")
