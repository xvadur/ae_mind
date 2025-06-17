# ae_mind: Modular Introspective Parser System for GPT Conversation Archives

## Overview

**ae_mind** is a modular, orchestrated, and audit-ready introspective parser system designed for advanced analysis of GPT conversation archives. It integrates with the Aethero government/agent structure, supports advanced linguistic and psychological analysis, and exports to Notion-ready formats. The system is built for long-term, scalable development and transparent project management.

---

## Features
- **Two-Phase Modular Pipeline:**
  - Phase 1: Linguistic Analysis (`phase1_linguistic_analyzer.py`)
  - Phase 2: Psychological Introspection (`phase2_psychological_introspector.py`)
- **Data Integration & Export:**
  - HTML, CSV, JSON, YAML, and Notion-ready formats (`aethero_memory_parser.py`)
- **Government/Agent Orchestration:**
  - Project management, analysis, and reporting via government/agent structure
- **Audit-Ready & Transparent:**
  - All analysis steps and agent/government records are tracked and exportable
- **Scalable & Extensible:**
  - Modular codebase, ready for advanced NLP/psychological modules and database connectors

---

## Folder Structure

```
ae_mind/
├── README.md
├── requirements.txt
├── constitution_monumentum_veritas.md
├── orchestration_alignment_report.md
├── government_meeting_2025-06-15.md
├── aethero_memory_parser.py
├── run_parser_demo.py
├── src/
│   ├── introspective_parser/
│   │   ├── phase1_linguistic_analyzer.py
│   │   └── phase2_psychological_introspector.py
│   └── ae_parser/   # AST/JSONC validation and traversal
├── agents/
│   ├── analyst_agent.md
│   ├── generator_agent.md
│   ├── planner_agent.md
│   ├── scout_agent.md
│   └── synthesis_agent.md
├── templates/
│   ├── ministerial_report.md
│   └── ministerial_report.html
```

---

## Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the parser demo:**
   ```bash
   python run_parser_demo.py
   ```
3. **Review outputs and reports in the specified output directory.**

---

## Government/Agent Orchestration
- See `government_meeting_2025-06-15.md`, `constitution_monumentum_veritas.md`, and `orchestration_alignment_report.md` for project management, agent roles, and orchestration logic.
- Agent templates and documentation are in `agents/`.

---

## Extending the System
- Add new analysis modules in `src/introspective_parser/`.
- Integrate new data formats or connectors in `aethero_memory_parser.py`.
- Update government/agent records and templates as needed.

---

## License
See `LICENSE` for details.

## n8n Integration

A custom node `aeMindNode` is provided in `n8n_node/aeMindNode.ts` to execute the parser within n8n workflows. It wraps the Python pipeline using `child_process` and returns the serialized `EthicalVectorBlock`.

### Example Usage
1. Compile the TypeScript file with `tsc`.
2. Copy the resulting JavaScript into your n8n custom nodes directory.
3. Import the node in your workflow. A sample workflow is provided in `test.n8n.json`.

## Docker Deployment

The `docker/` folder contains a `Dockerfile` used to build a parser image. A root
`docker-compose.yml` links this parser with an `n8n` container and mounts the
repository so the workflow can execute the pipeline.

Build and start the stack:

```bash
docker compose build
docker compose up
```

After the services start, open `http://localhost:5678` to configure the n8n
workflow. Import `aethero_pipeline_workflow.json` to get a ready-made HTTP
endpoint that triggers the parser.

## Configuration

Phase5 uses `phase5_config.yaml` to define model options and thresholds. Adjust this file to tune ethical vector generation.
