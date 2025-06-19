# AetheroOS – Digitálna vláda a agentický operačný systém

AetheroOS je moderný open-source framework pre vývoj, orchestráciu a introspektívne riadenie digitálnych agentov a multi-agentných workflowov. Projekt je navrhnutý ako hierarchická digitálna vláda s Premierom, ministerstvami, asistentskými agentmi, zdieľanou pamäťou a ústavou. Všetko je pripravené na škálovanie, rozširovanie a integráciu s AI, cloudom či externými API.

---

## Hlavné vlastnosti
- **Hierarchická architektúra:** Premier (orchestrátor), tajomníci, ministerstvá a asistenti podľa README_HIERARCHY.md
- **Zdieľaná pamäť:** Globálna a lokálna pamäť agentov, pripravená na integráciu s Notion, DB, cloudom
- **Ústava:** YAML/MD runtime ústava, ktorú systém načíta a môže dynamicky meniť
- **Plne rozšíriteľné:** Pridávaj ďalších agentov, workflowy, pamäťové moduly, API integrácie
- **Audit a introspekcia:** Každý krok workflowu je logovaný, všetky rozhodnutia sú spätne dohľadateľné
- **Kompatibilita s AI:** Pripravené na integráciu s OpenAI, smol-ai/developer, lsp-mcp a ďalšími AI nástrojmi

---

## Štruktúra projektu

```
aetheroos/
├── main_government.py         # Inicializácia a orchestrácia vlády
├── constitution/              # Ústava systému (YAML/MD)
├── memory/                    # Zdieľaná pamäť a moduly
├── agents/                    # Premier, ministri, asistenti, architektúra
├── ae_mind/                   # Parser, introspekcia, analytické moduly
├── aethero_agent_core/        # Klonované AI/agentické knižnice (developer, lsp-mcp)
├── openai-agents-python/      # OpenAI Agents SDK
├── ... ďalšie moduly ...
```

---

## Ako začať
1. Skontroluj README_HIERARCHY.md pre detailnú architektúru a onboarding
2. Nainštaluj závislosti: `pip install -r ae_mind/requirements.txt`
3. Spusť vládu: `python main_government.py`
4. Sleduj výstup, rozširuj workflowy, pridávaj agentov a integrácie

---

## Dokumentácia a rozvoj
- **README_HIERARCHY.md** – hlavný riadiaci dokument architektúry a rozvoja
- **agents/** – všetky triedy agentov, ministerstiev a asistentov
- **ae_mind/** – parser, introspekcia, analytické moduly
- **aethero_agent_core/** – AI knižnice, developer agent, lsp-mcp
- **openai-agents-python/** – orchestrácia agentov cez OpenAI SDK

---

## Príspevky a rozširovanie
Projekt je otvorený pre komunitu. Prispievaj cez pull requesty, issues alebo diskusie. Každý nový agent, workflow alebo integrácia je vítaná!

## Visual Studio Code Setup
Systém je možné pohodlne otvoriť vo [Visual Studio Code](https://code.visualstudio.com/) na lokálny vývoj.

### How to open in VSCode and run locally
1. Spusti VSCode v koreňovom adresári projektu:

```bash
code .
```

2. Nainštaluj závislosti:

```bash
pip install -r ae_mind/requirements.txt
```

3. Použi pripravenú VSCode konfiguráciu **Run Parser Pipeline** (`F5`), prípadne spusti manuálne:

```bash
python ae_mind/src/introspective_parser/run_pipeline.py INPUT_FILE --out output.md
```

Terminálový výstup bude dostupný priamo vo VSCode.

---

**AetheroOS – budúcnosť digitálnej vlády a agentických systémov.**
