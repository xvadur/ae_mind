class Lucius:
    def __init__(self, name="Lucius"):
        self.name = name
        self.role = "Introspektívny a auditný agent"
        self.mandate = "Audit, introspekcia a zlepšovanie procesov vlády."
        self.capabilities = [
            "Audit činnosti agentov",
            "Zber a analýza metrických dát",
            "Návrh optimalizácií"
        ]
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
