class MinisterOfExternalAffairs:
    def __init__(self, name="Minister Externých Vzťahov"):
        self.name = name
        self.role = "Externý integračný agent"
        self.mandate = "Správa a integrácia externých zdrojov a API."
        self.capabilities = [
            "Integrácia externých služieb",
            "Správa API kľúčov a prístupov",
            "Zabezpečenie komunikácie s externým svetom"
        ]
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
