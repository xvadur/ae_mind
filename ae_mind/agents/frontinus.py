class Frontinus:
    def __init__(self, name="Frontinus"):
        self.name = name
        self.role = "Agent pre strategické plánovanie"
        self.mandate = "Plánovanie, návrh a optimalizácia rozhraní a procesov."
        self.capabilities = [
            "Strategické plánovanie",
            "Návrh rozhraní",
            "Optimalizácia workflowov"
        ]
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
