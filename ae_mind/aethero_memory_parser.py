import os
import re
import csv
import json
import yaml
import uuid
from datetime import datetime
from bs4 import BeautifulSoup
import argparse

# Context tracker for conversation state
class ContextTracker:
    def __init__(self):
        self.current_date = None
        self.current_author = None
        self.tags = set()

    def update(self, date=None, author=None, tags=None):
        if date:
            self.current_date = date
        if author:
            self.current_author = author
        if tags:
            self.tags.update(tags)

    def get_context(self):
        return {
            'date': self.current_date,
            'author': self.current_author,
            'tags': list(self.tags)
        }

def parse_html_gpt_export(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Heuristic: each conversation block is a <div> with a certain class or structure
    # This may need to be adapted for your export format
    blocks = soup.find_all('div')
    conversations = []
    for block in blocks:
        text = block.get_text(separator='\n').strip()
        if not text:
            continue
        # Try to extract date, author, prompt, answer
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        date = date_match.group(1) if date_match else None
        author = 'Premier Aethero_X' if 'Aethero_X' in text else 'GPT'
        prompt_match = re.search(r'Prompt:(.*?)(Odpoveď:|$)', text, re.DOTALL)
        answer_match = re.search(r'Odpoveď:(.*)', text, re.DOTALL)
        prompt = prompt_match.group(1).strip() if prompt_match else ''
        answer = answer_match.group(1).strip() if answer_match else ''
        tags = []
        if 'gpt' in text.lower():
            tags.append('gpt')
        if 'prompt' in text.lower():
            tags.append('prompt')
        conversations.append({
            'date': date,
            'author': author,
            'prompt': prompt,
            'answer': answer,
            'tags': tags
        })
    return conversations

def export_markdown_yaml(conversations, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for conv in conversations:
        fname = f"{conv['date'] or 'unknown'}_{uuid.uuid4().hex[:8]}.md"
        path = os.path.join(out_dir, fname)
        frontmatter = {
            'date': conv['date'],
            'author': conv['author'],
            'tags': conv['tags']
        }
        with open(path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, allow_unicode=True)
            f.write('---\n\n')
            f.write(f"**Prompt:** {conv['prompt']}\n\n")
            f.write(f"**Odpoveď:** {conv['answer']}\n")

def export_csv(conversations, out_path):
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'author', 'prompt', 'answer', 'tags'])
        writer.writeheader()
        for conv in conversations:
            conv['tags'] = ','.join(conv['tags'])
            writer.writerow(conv)

def export_json(conversations, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Aethero Memory Parser – GPT Archive Processing Pipeline')
    parser.add_argument('input', help='Path to HTML export')
    parser.add_argument('--format', choices=['md', 'csv', 'json'], default='md', help='Output format')
    parser.add_argument('--out', default='aethero_memory_output', help='Output directory or file')
    args = parser.parse_args()

    conversations = parse_html_gpt_export(args.input)
    if args.format == 'md':
        export_markdown_yaml(conversations, args.out)
    elif args.format == 'csv':
        export_csv(conversations, args.out)
    elif args.format == 'json':
        export_json(conversations, args.out)
    print(f"Export complete: {args.out}")

if __name__ == '__main__':
    main()
