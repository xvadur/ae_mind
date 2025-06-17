class Vox:
    def __init__(self, name="Vox"):
        self.name = name
        self.role = "Komunikačný a jazykový agent"
        self.mandate = "Zabezpečiť komunikáciu, jazykové rozhranie a preklad medzi agentmi a používateľom."
        self.capabilities = [
            "Spracovanie prirodzeného jazyka",
            "Preklad a sumarizácia",
            "Komunikačné rozhranie systému"
        ]
        self.memory = []
    def activate(self):
        print(f"{self.name} bol aktivovaný.")
        self.memory.append("Aktivácia úspešná.")
    def report_capabilities(self):
        return f"Mandát: {self.mandate}\nSchopnosti: {', '.join(self.capabilities)}"
