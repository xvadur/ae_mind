class Implementus:
    def __init__(self, name="Implementus"):
        self.name = name
        self.role = "Výkonný agent pre implementáciu rozhodnutí"
        self.mandate = "Realizácia rozhodnutí vlády a koordinácia operatívnych úloh."
        self.capabilities = [
            "Implementácia workflowov",
            "Koordinácia operácií",
            "Monitorovanie priebehu úloh"
        ]
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
