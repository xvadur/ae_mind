from agents.premier import Premier
from agents.archivus import Archivus
from agents.vox import Vox
from agents.implementus import Implementus
from agents.lucius import Lucius
from agents.frontinus import Frontinus
from agents.minister_external import MinisterOfExternalAffairs

print("🕊️ Vitajte na inaugurácii vlády AetheroOS.")

# Premier
premier = Premier(name="Aethero_Xvadur")
print(f"\n🛡️ Premier {premier.name}:")
print(premier.report_capabilities())

# Archivus
archivus = Archivus(name="Archivus")
print(f"\n📚 Minister pamäte {archivus.name}:")
print(archivus.report_capabilities())

# Vox
vox = Vox(name="Vox Introspektra")
print(f"\n📣 Minister komunikácie {vox.name}:")
print(vox.report_capabilities())

# Implementus
implementus = Implementus(name="Implementus")
print(f"\n🛠️ Minister koordinácie {implementus.name}:")
print(implementus.report_capabilities())

# Lucius
lucius = Lucius(name="Lucius")
print(f"\n🧠 Minister vývoja {lucius.name}:")
print(lucius.report_capabilities())

# Frontinus
frontinus = Frontinus(name="Frontinus")
print(f"\n🎨 Minister rozhrania {frontinus.name}:")
print(frontinus.report_capabilities())

# Minister of External Affairs
external = MinisterOfExternalAffairs(name="Minister Externých Vzťahov")
print(f"\n🌐 Minister externých zdrojov {external.name}:")
print(external.report_capabilities())

print("\n✅ Všetci členovia vlády AetheroOS sú pripravení slúžiť.")
print("Zadajte úlohy, vytvorte Ústavu, a začnite budovať nový systém.")
