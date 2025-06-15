# ae_mind folder structure for migration
# This script (for reference) lists the copy/move operations needed to assemble the new ae_mind folder for repo import.
# You can run these commands from the aethero root directory.

mkdir -p ae_mind/src/introspective_parser
mkdir -p ae_mind/src/ae_parser
mkdir -p ae_mind/agents
mkdir -p ae_mind/templates

cp run_parser_demo.py ae_mind/
cp aethero_memory_parser.py ae_mind/
cp requirements.txt ae_mind/
cp constitution_monumentum_veritas.md ae_mind/
cp government_meeting_2025-06-15.md ae_mind/
cp orchestration_alignment_report.md ae_mind/
cp src/introspective_parser/phase1_linguistic_analyzer.py ae_mind/src/introspective_parser/
cp src/introspective_parser/phase2_psychological_introspector.py ae_mind/src/introspective_parser/
cp -R src/ae_parser/* ae_mind/src/ae_parser/
cp agents/analyst_agent.md ae_mind/agents/
cp agents/generator_agent.md ae_mind/agents/
cp agents/planner_agent.md ae_mind/agents/
cp agents/scout_agent.md ae_mind/agents/
cp agents/synthesis_agent.md ae_mind/agents/
cp templates/ministerial_report.md ae_mind/templates/
cp templates/ministerial_report.html ae_mind/templates/
cp ae_mind/README.md ae_mind/
cp ae_mind/ONBOARDING.md ae_mind/
cp ae_mind/MIGRATION_CHECKLIST.txt ae_mind/
cp ae_mind/__init__.py ae_mind/

# (Optional: add more cp commands for docs, sample data, etc.)
