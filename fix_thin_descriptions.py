#!/usr/bin/env python3
"""
Fix thin meta descriptions on Manhattan site.
Make each page's description unique and detailed.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

# Varied description templates - more variety
TEMPLATES = [
    "Expert appliance repair in {location}, Manhattan. Same-day service for refrigerators, ovens, dishwashers, washers & dryers. Factory-certified technicians.",
    "Professional appliance repair services in {location}, NY. Fast response, all major brands. Call now for same-day appointments.",
    "{location} appliance repair specialists serving Manhattan. Trusted for reliable washer, dryer, refrigerator, and oven repairs. Licensed & insured.",
    "Need appliance repair in {location}? Our certified technicians offer same-day service for all major brands in the {location} area.",
    "Top-rated appliance repair in {location}, Manhattan. We fix refrigerators, dishwashers, ovens, washers, dryers & more. Call today!",
    "Affordable appliance repair in {location}, NY. Experienced technicians, upfront pricing, fast turnaround. Serving {location} residents daily.",
    "{location} homeowners trust us for appliance repairs. Refrigerators, stoves, washers, dryers - all brands serviced. Same-day available.",
    "Local appliance repair experts in {location}, Manhattan. Quick diagnosis, quality parts, lasting repairs. Book your appointment now.",
    "Dependable appliance repair service in {location}. We repair all major appliances - refrigerators, ovens, dishwashers, and more.",
    "Manhattan's trusted appliance repair in {location}. Professional service, competitive rates, same-day appointments available.",
]

def format_location(slug):
    """Convert slug to proper location name."""
    return slug.replace("-", " ").title()

def get_template_index(location):
    """Get consistent but varied template index based on location name."""
    hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
    return hash_val % len(TEMPLATES)

def fix_description(file_path):
    """Fix thin meta description in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Get location from path
    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    if len(parts) < 2 or parts[0] != 'ny':
        return False

    location = format_location(parts[1])
    template_idx = get_template_index(location)
    template = TEMPLATES[template_idx]
    new_desc = template.format(location=location)

    # Replace meta description
    new_content = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="{new_desc}"',
        content
    )

    # Also fix og:description
    if 'og:description' in new_content:
        new_content = re.sub(
            r'<meta property="og:description" content="[^"]*"',
            f'<meta property="og:description" content="{new_desc}"',
            new_content
        )

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True

    return False


def main():
    # Find all location pages in ny/
    ny_dir = BASE_DIR / 'ny'
    if not ny_dir.exists():
        print("No ny/ directory found")
        return

    html_files = list(ny_dir.rglob('index.html'))
    print(f"Found {len(html_files)} pages in ny/")

    fixed = 0
    for html_file in html_files:
        if fix_description(html_file):
            fixed += 1

    print(f"Fixed {fixed} descriptions with varied templates")


if __name__ == "__main__":
    main()
