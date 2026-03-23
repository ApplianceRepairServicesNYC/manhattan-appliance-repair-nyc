#!/usr/bin/env python3
"""Fix short meta descriptions for appliances and brands pages"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/Users/globalaffiliate/manhattan-appliance-repair-nyc")

# Better descriptions for appliances
APPLIANCE_DESCRIPTIONS = {
    'refrigerator-repair': 'Expert refrigerator repair in Manhattan NY. Same-day service for all brands. Certified technicians, upfront pricing. Call now!',
    'oven-repair': 'Professional oven repair in Manhattan NY. Gas & electric ovens serviced same-day. All major brands. Book your appointment today!',
    'dishwasher-repair': 'Fast dishwasher repair in Manhattan NY. Same-day appointments available. All brands serviced by certified technicians. Call now!',
    'wine-cooler-repair': 'Wine cooler repair specialists in Manhattan NY. Protect your collection with same-day service. All brands. Call for a free estimate!',
    'vent-hood-repair': 'Vent hood repair in Manhattan NY. Range hood & exhaust fan service. Same-day appointments. Certified technicians. Call today!',
    'washer-repair': 'Washer repair in Manhattan NY. Top-load & front-load washers serviced same-day. All brands. Certified technicians. Book now!',
    'microwave-repair': 'Microwave repair in Manhattan NY. Countertop & built-in microwaves fixed same-day. All brands serviced. Call for fast service!',
    'cooktop-repair': 'Cooktop repair in Manhattan NY. Gas & electric cooktops serviced same-day. All brands. Certified technicians. Call now!',
    'dryer-repair': 'Dryer repair in Manhattan NY. Gas & electric dryers fixed same-day. All major brands. Certified technicians. Book today!',
    'installation-maintenance': 'Appliance installation & maintenance in Manhattan NY. Professional setup for all major brands. Same-day service available!',
}

def fix_appliance_meta(filepath, appliance_type):
    """Fix meta description for appliance pages"""
    if appliance_type not in APPLIANCE_DESCRIPTIONS:
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        new_desc = APPLIANCE_DESCRIPTIONS[appliance_type]
        # Replace short meta description
        html = re.sub(
            r'<meta name="description" content="[^"]{0,70}">',
            f'<meta name="description" content="{new_desc}">',
            html
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    except:
        return False

def fix_brand_meta(filepath, brand_name):
    """Fix meta description for brand pages"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Check if meta description is short
        match = re.search(r'<meta name="description" content="([^"]*)">', html)
        if not match or len(match.group(1)) >= 70:
            return False

        new_desc = f"Expert {brand_name} appliance repair in Manhattan NY. Same-day service, certified technicians, genuine parts. Call for a free estimate!"
        html = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{new_desc}">',
            html
        )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    except:
        return False

def main():
    count = 0

    # Fix appliance pages
    appliances_dir = BASE_DIR / 'appliances'
    for subdir in appliances_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                if fix_appliance_meta(index_file, subdir.name):
                    count += 1

    # Fix brand pages (main brand page only, not subpages)
    brands_dir = BASE_DIR / 'brands'
    for subdir in brands_dir.iterdir():
        if subdir.is_dir():
            index_file = subdir / 'index.html'
            if index_file.exists():
                brand_name = subdir.name.replace('-', ' ').title()
                # Handle special cases
                brand_name = brand_name.replace('Lg', 'LG').replace('Ge', 'GE').replace('Aeg', 'AEG')
                brand_name = brand_name.replace('Ikea', 'IKEA').replace('Sub Zero', 'Sub-Zero')
                if fix_brand_meta(index_file, brand_name):
                    count += 1

    # Fix other pages with short descriptions
    other_pages = [
        (BASE_DIR / 'privacy-policy' / 'index.html', 'Read our privacy policy. Manhattan Appliance Repair NYC protects your personal information. Learn how we handle your data.'),
        (BASE_DIR / 'terms-of-service' / 'index.html', 'Terms of service for Manhattan Appliance Repair NYC. Read our service agreement, warranty terms, and repair policies.'),
        (BASE_DIR / 'repairs' / 'refrigerator-compressor-replacement' / 'index.html', 'Refrigerator compressor replacement in Manhattan NY. Expert diagnosis, quality parts, same-day service. Call for a free estimate!'),
        (BASE_DIR / 'troubleshooting' / 'appliance-troubleshooting' / 'index.html', 'Appliance troubleshooting guide for Manhattan NY residents. DIY tips and when to call a professional. Free diagnosis available!'),
    ]

    for filepath, new_desc in other_pages:
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html = f.read()
                html = re.sub(
                    r'<meta name="description" content="[^"]*">',
                    f'<meta name="description" content="{new_desc}">',
                    html
                )
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                count += 1
            except:
                pass

    print(f"Updated {count} meta descriptions")

if __name__ == '__main__':
    main()
