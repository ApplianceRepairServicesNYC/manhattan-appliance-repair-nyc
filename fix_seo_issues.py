#!/usr/bin/env python3
"""Fix SEO issues: short titles and duplicate meta descriptions"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/Users/globalaffiliate/manhattan-appliance-repair-nyc")

def fix_title(html, filepath):
    """Add ' | Same Day Service' to short titles"""
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if not title_match:
        return html

    title = title_match.group(1)

    # Skip if already has suffix or is long enough
    if '| Same Day' in title or '| Manhattan' in title or len(title) >= 35:
        return html

    # Skip certain pages
    skip_patterns = ['Privacy Policy', 'Terms of Service', 'Sitemap', '404', 'Page Not Found']
    if any(p in title for p in skip_patterns):
        return html

    new_title = f"{title} | Same Day Service"
    html = html.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
    return html


def fix_meta_description(html, filepath):
    """Make meta descriptions unique for service subpages"""
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
    if not desc_match:
        return html

    current_desc = desc_match.group(1)
    path_parts = str(filepath).split('/')

    # Determine page type from path
    is_brand_service = 'brands' in path_parts and len(path_parts) > path_parts.index('brands') + 2
    is_neighborhood_service = 'ny' in path_parts and len(path_parts) > path_parts.index('ny') + 2

    if is_neighborhood_service:
        # Extract neighborhood and service
        ny_idx = path_parts.index('ny')
        neighborhood = path_parts[ny_idx + 1].replace('-', ' ').title()
        service_folder = path_parts[ny_idx + 2] if ny_idx + 2 < len(path_parts) else ''

        if service_folder and service_folder != 'index.html':
            service = service_folder.replace('-repair', '').replace('-', ' ').title()

            # Create unique description for service page
            if 'repair' in service_folder:
                new_desc = f"Expert {service} repair service in {neighborhood}, Manhattan. Same-day appointments, certified technicians, all major brands. Call now for fast service!"
            else:
                new_desc = f"Professional {service} service in {neighborhood}, Manhattan. Certified technicians, upfront pricing. Book your appointment today!"

            html = html.replace(f'content="{current_desc}"', f'content="{new_desc}"')

    elif is_brand_service:
        # Extract brand and service
        brand_idx = path_parts.index('brands')
        brand = path_parts[brand_idx + 1].replace('-', ' ').title()
        service_folder = path_parts[brand_idx + 2] if brand_idx + 2 < len(path_parts) else ''

        if service_folder and service_folder != 'index.html':
            service = service_folder.replace('-repair', '').replace('-', ' ').title()

            new_desc = f"Manhattan's trusted {brand} {service.lower()} repair experts. Factory-trained technicians, genuine parts, same-day service available. Call for a free estimate!"
            html = html.replace(f'content="{current_desc}"', f'content="{new_desc}"')

    return html


def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        original = html
        html = fix_title(html, filepath)
        html = fix_meta_description(html, filepath)

        if html != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    count = 0
    # Process neighborhood pages
    ny_dir = BASE_DIR / 'ny'
    for html_file in ny_dir.rglob('index.html'):
        if process_file(html_file):
            count += 1

    # Process brand pages
    brands_dir = BASE_DIR / 'brands'
    for html_file in brands_dir.rglob('index.html'):
        if process_file(html_file):
            count += 1

    # Process appliance pages
    appliances_dir = BASE_DIR / 'appliances'
    for html_file in appliances_dir.rglob('index.html'):
        if process_file(html_file):
            count += 1

    print(f"Updated {count} files")


if __name__ == '__main__':
    main()
