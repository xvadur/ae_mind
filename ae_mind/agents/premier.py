from agents.archivus import Archivus
from agents.vox import Vox
from agents.implementus import Implementus
from agents.lucius import Lucius
from agents.frontinus import Frontinus
from agents.minister_external import MinisterExternal

class Premier:
    def __init__(self, name="Premier Aethero_Xvadur"):
        self.name = name
        self.role = "Koordinátor vlády a strategický líder"
        self.mandate = "Zabezpečiť súhru, strategické smerovanie a ochranu integrity systému."
        self.capabilities = [
            "Koordinácia agentov a workflowov",
            "Strategické rozhodovanie",
            "Audit a introspekcia vlády"
        ]
        self.council = [
            Archivus(), Vox(), Implementus(), Lucius(), Frontinus(), MinisterExternal()
        ]
        self.memory = []
        self.audit_log = []

    def summon_council(self):
        print(f"{self.name} zvoláva vládu Aethero.")
        for agent in self.council:
            agent.activate()
            self.memory.append(f"{agent.name} aktivovaný.")
        print("Vláda bola úspešne inicializovaná.")

    def introspect_government(self):
        print("\n[INTROSPEKCIA] Audit vlády:")
        for entry in self.memory:
            print(f" - {entry}")
        print("[INTROSPEKCIA] Všetci agenti pripravení na výkon.")

    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
