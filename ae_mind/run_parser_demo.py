"""
run_parser_demo.py – Entry point pre dvojfázový introspektívny parser
"""
from src.introspective_parser.phase1_linguistic_analyzer import Phase1LinguisticAnalyzer
from src.introspective_parser.phase2_psychological_introspector import Phase2PsychologicalIntrospector
from src.ae_parser import main as ae_parser_main
import argparse
import os
import json

def main():
    parser = argparse.ArgumentParser(description='Aethero Introspective Parser Demo')
    parser.add_argument('--input', required=True, help='Cesta k vstupnému súboru (HTML alebo JSON)')
    parser.add_argument('--output', required=True, help='Cesta k výstupnému adresáru')
    args = parser.parse_args()

    # Fáza 1: Jazyková a štruktúrna analýza
    phase1 = Phase1LinguisticAnalyzer()
    linguistic_results = phase1.process(args.input)

    # Fáza 2: Psychologická introspekcia
    phase2 = Phase2PsychologicalIntrospector()
    psychological_results = phase2.process(linguistic_results)

    # Export výsledkov (Markdown + YAML frontmatter + JSON)
    os.makedirs(args.output, exist_ok=True)
    for idx, result in enumerate(psychological_results):
        # YAML + Markdown
        yaml_header = result['yaml_header']
        markdown_body = result['markdown_body']
        with open(os.path.join(args.output, f'conversation_{idx+1}.md'), 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(yaml_header)
            f.write('---\n\n')
            f.write(markdown_body)
        # JSON
        with open(os.path.join(args.output, f'conversation_{idx+1}.json'), 'w', encoding='utf-8') as f:
            json.dump(result['json'], f, ensure_ascii=False, indent=2)
    print(f"Spracovanie dokončené. Výstup uložený v {args.output}")

if __name__ == '__main__':
    main()
