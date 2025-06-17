class Archivus:
    def __init__(self, name="Archivus"):
        self.name = name
        self.role = "Pamäťový a analytický agent"
        self.mandate = "Správa, uchovávanie a analýza pamäťových záznamov systému."
        self.capabilities = [
            "Ukladanie a vyhľadávanie dát",
            "Analýza historických záznamov",
            "Podpora introspekcie agentov"
        ]
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
