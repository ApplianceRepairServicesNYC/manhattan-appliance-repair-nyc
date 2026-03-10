#!/usr/bin/env python3
"""
Move the schedule form section to appear BEFORE the 3 buttons section.
"""

import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

def move_form(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if no schedule form section
    if '<!-- SCHEDULE FORM SECTION -->' not in content:
        return False

    # Skip if no 3 buttons section (identified by "All Repair Services" in a section)
    if 'All Repair Services</span>' not in content:
        return False

    # Extract the schedule form section
    form_match = re.search(
        r'(<!-- SCHEDULE FORM SECTION -->.*?<!-- END SCHEDULE FORM SECTION -->)',
        content,
        re.DOTALL
    )
    if not form_match:
        return False

    form_section = form_match.group(1)

    # Remove the form section from its current location
    content_without_form = content.replace(form_section, '')

    # Find the 3 buttons section and insert form before it
    # The buttons section pattern
    buttons_pattern = r'(<section style="padding: 35px 0; background: linear-gradient\(135deg, #f8f9fa 0%, #e9ecef 100%\);">.*?All Repair Services</span>.*?</section>)'

    buttons_match = re.search(buttons_pattern, content_without_form, re.DOTALL)
    if not buttons_match:
        return False

    # Insert form section before the buttons section
    buttons_section = buttons_match.group(1)
    new_content = content_without_form.replace(
        buttons_section,
        form_section + '\n\n' + buttons_section
    )

    # Only write if content changed
    if new_content == content:
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if move_form(f):
            count += 1

    print(f"Moved form before buttons on {count} pages")


if __name__ == "__main__":
    main()
