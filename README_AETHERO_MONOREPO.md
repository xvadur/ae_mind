# Aethero Agent Core – Monorepo

## Úvod
Tento monorepo projekt integruje viacero špičkových open-source komponentov pre vývoj autonómnych AI agentov, orchestráciu, introspektívnu analýzu a prácu s kontextom kódu. Cieľom je vytvoriť robustný základ pre systém AetheroOS, ktorý umožňuje:
- Orchestráciu multi-agentných workflowov
- Pokročilú introspektívnu analýzu textov a kódu
- Dynamickú pamäť a kontextovú vrstvu pre AI agentov
- Jednoduchú rozšíriteľnosť a integráciu ďalších nástrojov

## Zahrnuté repozitáre a ich úloha

### 1. `ae_mind` (jsonc-parser)
- **Popis:** Scanner a parser pre JSON s komentármi (JSONC). Umožňuje tokenizáciu, SAX-style parsing, DOM parsing, formátovanie a modifikáciu JSON/JSONC dokumentov.
- **Využitie:** Základná analytická a parserová vrstva pre štruktúrované dáta a konfigurácie v rámci systému.

### 2. `openai-agents-python`
- **Popis:** Oficiálny OpenAI Agents SDK pre Python. Umožňuje definovať, orchestrálne riadiť a monitorovať AI agentov, ich workflowy, handoffy, guardrails a tracing.
- **Využitie:** Orchestrácia agentov, workflow management, bezpečnostné guardrails, tracing a debugging agentných procesov.

### 3. `lsp-mcp`
- **Popis:** Model Context Protocol (MCP) server, ktorý poskytuje AI agentom jazykovo-štruktúrovaný kontext z kódu (LSP-like API). Umožňuje AI agentom analyzovať, vyhľadávať a získavať informácie z veľkých codebase.
- **Využitie:** Dynamická pamäťová a kontextová vrstva pre agentov, introspektívna analýza kódu, podpora pre LLM a AI workflowy.

### 4. `developer` (smol-ai/developer)
- **Popis:** (README sa nenašiel, popis podľa známych informácií) Python knižnica na embedovanie autonómneho "developer agenta" do aplikácie. Umožňuje AI asistenciu pri generovaní kódu, návrhu architektúry, odpovediach na technické otázky a automatizovaných operáciách.
- **Využitie:** AI developer asistent, generovanie kódu, automatizácia vývojárskych úloh, rozšíriteľnosť systému o ďalšie AI schopnosti.

## Prvý projekt: AetheroOS MVP
Cieľom je vytvoriť MVP systému AetheroOS, ktorý:
- Orchestruje AI agentov (cez openai-agents-python)
- Využíva introspektívny parser (ae_mind) na analýzu textov a dát
- Má dynamickú pamäťovú vrstvu (lsp-mcp)
- Umožňuje AI developer asistenciu (developer)
- Je pripravený na rozšírenie o ďalšie workflowy, integrácie a analytické moduly

## Ako začať
1. Preštuduj README každého repozitára pre detailné API a príklady.
2. Nainštaluj závislosti podľa jednotlivých README (pip/npm).
3. Spusti základné príklady a over integráciu medzi komponentmi.
4. Začni s návrhom vlastného workflowu v rámci AetheroOS podľa svojich potrieb.

---
Tento README je úvodným rozcestníkom pre orientáciu v monorepe a ďalší rozvoj projektu.
