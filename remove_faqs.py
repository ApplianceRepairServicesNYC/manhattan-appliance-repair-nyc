#!/usr/bin/env python3
"""
Remove FAQ sections from all pages.
"""

import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

def remove_faqs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    original = content

    # Remove FAQ heading and all FAQ divs that follow
    # Pattern 1: FAQ heading with following divs
    content = re.sub(
        r'<h3[^>]*>Frequently Asked Questions[^<]*</h3>\s*(?:<div[^>]*>.*?</div>\s*)*',
        '',
        content,
        flags=re.DOTALL
    )

    # Pattern 2: Individual FAQ divs with questions
    content = re.sub(
        r'<div style="margin-bottom: 15px; padding: 12px; background: #f8f9fa; border-radius: 6px;">\s*<strong[^>]*>[^<]*\?</strong>\s*<p[^>]*>[^<]*</p>\s*</div>',
        '',
        content
    )

    # Pattern 3: FAQ divs with 20px margin
    content = re.sub(
        r'<div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">\s*<h4[^>]*>[^<]*\?</h4>\s*<p[^>]*>[^<]*</p>\s*</div>',
        '',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    count = 0
    for f in html_files:
        if remove_faqs(f):
            count += 1
    print(f"Removed FAQs from {count} pages")

if __name__ == "__main__":
    main()
