# ae_mind Onboarding Guide

Welcome to the **ae_mind** project! This guide will help you get started with development, testing, and contributing to the modular introspective parser system for GPT conversation archives.

---

## 1. Project Setup

- Clone or copy the `ae_mind` folder into your desired workspace or repository.
- Ensure you have Python 3.9+ installed.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

## 2. Running the Parser Pipeline

- The main entry point is `run_parser_demo.py`.
- This script orchestrates the two-phase pipeline:
  - **Phase 1:** Linguistic analysis
  - **Phase 2:** Psychological introspection
- Outputs are generated in the specified output directory or as configured in the script.

---

## 3. Project Structure

- `src/introspective_parser/`: Core analysis modules
- `src/ae_parser/`: AST/JSONC validation and traversal
- `aethero_memory_parser.py`: Data integration and export
- `agents/`: Agent/government documentation and templates
- `templates/`: Reporting templates
- `government_meeting_2025-06-15.md`, `constitution_monumentum_veritas.md`, `orchestration_alignment_report.md`: Project management and orchestration records

---

## 4. Government/Agent Orchestration

- The project uses a government/agent structure for transparent, auditable project management.
- See the government meeting and constitution files for roles, responsibilities, and reporting templates.

---

## 5. Extending & Contributing

- Add new analysis modules in `src/introspective_parser/`.
- Update or add agent/government documentation in `agents/`.
- Use the provided templates for new reports or outputs.
- All contributions should be auditable and documented per the government structure.

---

## 6. Support

- For questions, see the documentation in `docs/` or contact the project maintainers listed in the government records.

---

Happy hacking!
