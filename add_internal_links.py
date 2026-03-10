#!/usr/bin/env python3
"""
Add contextual internal links to all pages for better SEO link building.
Similar to wolf-bergen-county's approach.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')
SITE_URL = 'https://manhattanappliancerepairnyc.com'

# Manhattan neighborhoods with nearby neighborhoods
NEIGHBORHOODS = {
    'alphabet-city': {'name': 'Alphabet City', 'nearby': ['east-village', 'lower-east-side', 'bowery']},
    'battery-park-city': {'name': 'Battery Park City', 'nearby': ['tribeca', 'financial-district', 'world-trade-center']},
    'bloomingdale': {'name': 'Bloomingdale', 'nearby': ['upper-west-side', 'manhattan-valley', 'morningside-heights']},
    'bowery': {'name': 'Bowery', 'nearby': ['east-village', 'noho', 'lower-east-side']},
    'bryant-park': {'name': 'Bryant Park', 'nearby': ['midtown', 'times-square', 'garment-district']},
    'carnegie-hill': {'name': 'Carnegie Hill', 'nearby': ['upper-east-side', 'yorkville', 'lenox-hill']},
    'central-harlem': {'name': 'Central Harlem', 'nearby': ['harlem', 'east-harlem', 'morningside-heights']},
    'central-park-south': {'name': 'Central Park South', 'nearby': ['midtown', 'upper-west-side', 'upper-east-side']},
    'chelsea': {'name': 'Chelsea', 'nearby': ['west-village', 'flatiron-district', 'hudson-yards']},
    'chinatown': {'name': 'Chinatown', 'nearby': ['little-italy', 'lower-east-side', 'tribeca']},
    'civic-center': {'name': 'Civic Center', 'nearby': ['tribeca', 'chinatown', 'financial-district']},
    'columbus-circle': {'name': 'Columbus Circle', 'nearby': ['upper-west-side', 'midtown', 'central-park-south']},
    'east-harlem': {'name': 'East Harlem', 'nearby': ['harlem', 'central-harlem', 'yorkville']},
    'east-village': {'name': 'East Village', 'nearby': ['alphabet-city', 'west-village', 'noho']},
    'financial-district': {'name': 'Financial District', 'nearby': ['battery-park-city', 'tribeca', 'world-trade-center']},
    'flatiron-district': {'name': 'Flatiron District', 'nearby': ['gramercy', 'chelsea', 'nomad']},
    'fort-george': {'name': 'Fort George', 'nearby': ['washington-heights', 'inwood', 'hudson-heights']},
    'garment-district': {'name': 'Garment District', 'nearby': ['midtown', 'times-square', 'koreatown']},
    'gramercy': {'name': 'Gramercy', 'nearby': ['flatiron-district', 'kips-bay', 'murray-hill']},
    'greenwich-village': {'name': 'Greenwich Village', 'nearby': ['west-village', 'noho', 'soho']},
    'hamilton-heights': {'name': 'Hamilton Heights', 'nearby': ['harlem', 'washington-heights', 'sugar-hill']},
    'harlem': {'name': 'Harlem', 'nearby': ['central-harlem', 'east-harlem', 'hamilton-heights']},
    'hells-kitchen': {'name': "Hell's Kitchen", 'nearby': ['midtown', 'times-square', 'hudson-yards']},
    'herald-square': {'name': 'Herald Square', 'nearby': ['midtown', 'koreatown', 'garment-district']},
    'hudson-heights': {'name': 'Hudson Heights', 'nearby': ['washington-heights', 'fort-george', 'inwood']},
    'hudson-square': {'name': 'Hudson Square', 'nearby': ['soho', 'tribeca', 'west-village']},
    'hudson-yards': {'name': 'Hudson Yards', 'nearby': ['chelsea', 'hells-kitchen', 'midtown']},
    'inwood': {'name': 'Inwood', 'nearby': ['washington-heights', 'fort-george', 'hudson-heights']},
    'kips-bay': {'name': 'Kips Bay', 'nearby': ['murray-hill', 'gramercy', 'stuyvesant-town']},
    'koreatown': {'name': 'Koreatown', 'nearby': ['midtown', 'herald-square', 'nomad']},
    'lenox-hill': {'name': 'Lenox Hill', 'nearby': ['upper-east-side', 'yorkville', 'carnegie-hill']},
    'lincoln-square': {'name': 'Lincoln Square', 'nearby': ['upper-west-side', 'columbus-circle', 'manhattan-valley']},
    'little-italy': {'name': 'Little Italy', 'nearby': ['chinatown', 'soho', 'nolita']},
    'lower-east-side': {'name': 'Lower East Side', 'nearby': ['chinatown', 'east-village', 'alphabet-city']},
    'manhattan-valley': {'name': 'Manhattan Valley', 'nearby': ['upper-west-side', 'morningside-heights', 'bloomingdale']},
    'meatpacking-district': {'name': 'Meatpacking District', 'nearby': ['west-village', 'chelsea', 'hudson-yards']},
    'midtown': {'name': 'Midtown', 'nearby': ['times-square', 'bryant-park', 'herald-square']},
    'midtown-east': {'name': 'Midtown East', 'nearby': ['midtown', 'murray-hill', 'turtle-bay']},
    'morningside-heights': {'name': 'Morningside Heights', 'nearby': ['harlem', 'manhattan-valley', 'upper-west-side']},
    'murray-hill': {'name': 'Murray Hill', 'nearby': ['kips-bay', 'midtown-east', 'gramercy']},
    'noho': {'name': 'NoHo', 'nearby': ['greenwich-village', 'east-village', 'soho']},
    'nolita': {'name': 'NoLita', 'nearby': ['little-italy', 'soho', 'bowery']},
    'nomad': {'name': 'NoMad', 'nearby': ['flatiron-district', 'koreatown', 'murray-hill']},
    'roosevelt-island': {'name': 'Roosevelt Island', 'nearby': ['upper-east-side', 'midtown-east', 'yorkville']},
    'soho': {'name': 'SoHo', 'nearby': ['tribeca', 'greenwich-village', 'nolita']},
    'stuyvesant-town': {'name': 'Stuyvesant Town', 'nearby': ['gramercy', 'kips-bay', 'east-village']},
    'sugar-hill': {'name': 'Sugar Hill', 'nearby': ['hamilton-heights', 'harlem', 'washington-heights']},
    'sutton-place': {'name': 'Sutton Place', 'nearby': ['midtown-east', 'turtle-bay', 'upper-east-side']},
    'times-square': {'name': 'Times Square', 'nearby': ['midtown', 'hells-kitchen', 'bryant-park']},
    'tribeca': {'name': 'Tribeca', 'nearby': ['soho', 'financial-district', 'battery-park-city']},
    'turtle-bay': {'name': 'Turtle Bay', 'nearby': ['midtown-east', 'sutton-place', 'murray-hill']},
    'two-bridges': {'name': 'Two Bridges', 'nearby': ['chinatown', 'lower-east-side', 'financial-district']},
    'union-square': {'name': 'Union Square', 'nearby': ['gramercy', 'flatiron-district', 'greenwich-village']},
    'upper-east-side': {'name': 'Upper East Side', 'nearby': ['yorkville', 'lenox-hill', 'carnegie-hill']},
    'upper-west-side': {'name': 'Upper West Side', 'nearby': ['lincoln-square', 'manhattan-valley', 'morningside-heights']},
    'washington-heights': {'name': 'Washington Heights', 'nearby': ['inwood', 'hudson-heights', 'hamilton-heights']},
    'west-village': {'name': 'West Village', 'nearby': ['greenwich-village', 'chelsea', 'meatpacking-district']},
    'world-trade-center': {'name': 'World Trade Center', 'nearby': ['financial-district', 'battery-park-city', 'tribeca']},
    'yorkville': {'name': 'Yorkville', 'nearby': ['upper-east-side', 'lenox-hill', 'carnegie-hill']},
}

# Appliance types for cross-linking
APPLIANCES = [
    ('refrigerator-repair', 'refrigerator repair'),
    ('washer-repair', 'washer repair'),
    ('dryer-repair', 'dryer repair'),
    ('dishwasher-repair', 'dishwasher repair'),
    ('oven-repair', 'oven repair'),
    ('cooktop-repair', 'cooktop repair'),
]

# Major brands for cross-linking
BRANDS = [
    ('lg', 'LG'),
    ('samsung', 'Samsung'),
    ('whirlpool', 'Whirlpool'),
    ('ge', 'GE'),
    ('bosch', 'Bosch'),
    ('kitchenaid', 'KitchenAid'),
    ('frigidaire', 'Frigidaire'),
    ('maytag', 'Maytag'),
]

def get_hash_index(text, num_options):
    """Get deterministic index based on hash."""
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % num_options


def add_neighborhood_links(content, neighborhood_slug):
    """Add contextual links to a neighborhood page."""
    if neighborhood_slug not in NEIGHBORHOODS:
        return content, False

    info = NEIGHBORHOODS[neighborhood_slug]
    name = info['name']
    nearby = info['nearby']

    # Filter to only existing nearby neighborhoods
    valid_nearby = [n for n in nearby if n in NEIGHBORHOODS]
    if not valid_nearby:
        return content, False

    # Pick 2 nearby neighborhoods based on hash
    idx1 = get_hash_index(neighborhood_slug + "1", len(valid_nearby))
    idx2 = get_hash_index(neighborhood_slug + "2", len(valid_nearby))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(valid_nearby)

    nearby1 = valid_nearby[idx1]
    nearby2 = valid_nearby[idx2]
    nearby1_name = NEIGHBORHOODS[nearby1]['name']
    nearby2_name = NEIGHBORHOODS[nearby2]['name']

    # Pick an appliance and brand
    app_idx = get_hash_index(neighborhood_slug + "app", len(APPLIANCES))
    brand_idx = get_hash_index(neighborhood_slug + "brand", len(BRANDS))
    appliance_slug, appliance_name = APPLIANCES[app_idx]
    brand_slug, brand_name = BRANDS[brand_idx]

    # Build the links paragraph
    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">We proudly serve {name} and neighboring areas including <a href="{SITE_URL}/ny/{nearby1}/">{nearby1_name}</a> and <a href="{SITE_URL}/ny/{nearby2}/">{nearby2_name}</a>. Our technicians are experts in <a href="{SITE_URL}/appliances/{appliance_slug}/">{appliance_name}</a> and all <a href="{SITE_URL}/brands/{brand_slug}/">{brand_name} appliances</a>.</p>
'''

    # Find the unique content section and add links before the closing </div>
    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Check if links already added
        if 'proudly serve' in match.group(2) and '/ny/' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def add_brand_links(content, brand_slug):
    """Add contextual links to a brand page."""
    # Pick 2 random neighborhoods
    neighborhood_list = list(NEIGHBORHOODS.keys())
    idx1 = get_hash_index(brand_slug + "n1", len(neighborhood_list))
    idx2 = get_hash_index(brand_slug + "n2", len(neighborhood_list))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(neighborhood_list)

    n1 = neighborhood_list[idx1]
    n2 = neighborhood_list[idx2]
    n1_name = NEIGHBORHOODS[n1]['name']
    n2_name = NEIGHBORHOODS[n2]['name']

    # Pick an appliance
    app_idx = get_hash_index(brand_slug + "app", len(APPLIANCES))
    appliance_slug, appliance_name = APPLIANCES[app_idx]

    # Get brand name
    brand_name = brand_slug.upper()
    for b_slug, b_name in BRANDS:
        if b_slug == brand_slug:
            brand_name = b_name
            break

    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">Our {brand_name} repair services cover all Manhattan neighborhoods including <a href="{SITE_URL}/ny/{n1}/">{n1_name}</a> and <a href="{SITE_URL}/ny/{n2}/">{n2_name}</a>. We specialize in <a href="{SITE_URL}/appliances/{appliance_slug}/">{appliance_name}</a> for {brand_name} and all major brands.</p>
'''

    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        if 'repair services cover' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def add_appliance_links(content, appliance_slug):
    """Add contextual links to an appliance page."""
    # Pick 2 random neighborhoods
    neighborhood_list = list(NEIGHBORHOODS.keys())
    idx1 = get_hash_index(appliance_slug + "n1", len(neighborhood_list))
    idx2 = get_hash_index(appliance_slug + "n2", len(neighborhood_list))
    if idx2 == idx1:
        idx2 = (idx1 + 1) % len(neighborhood_list)

    n1 = neighborhood_list[idx1]
    n2 = neighborhood_list[idx2]
    n1_name = NEIGHBORHOODS[n1]['name']
    n2_name = NEIGHBORHOODS[n2]['name']

    # Pick 2 brands
    brand_idx1 = get_hash_index(appliance_slug + "b1", len(BRANDS))
    brand_idx2 = get_hash_index(appliance_slug + "b2", len(BRANDS))
    if brand_idx2 == brand_idx1:
        brand_idx2 = (brand_idx1 + 1) % len(BRANDS)

    brand1_slug, brand1_name = BRANDS[brand_idx1]
    brand2_slug, brand2_name = BRANDS[brand_idx2]

    # Get appliance name
    appliance_name = appliance_slug.replace('-', ' ').title()

    links_html = f'''
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">Our {appliance_name.lower()} services are available throughout Manhattan including <a href="{SITE_URL}/ny/{n1}/">{n1_name}</a> and <a href="{SITE_URL}/ny/{n2}/">{n2_name}</a>. We repair all major brands including <a href="{SITE_URL}/brands/{brand1_slug}/">{brand1_name}</a> and <a href="{SITE_URL}/brands/{brand2_slug}/">{brand2_name}</a>.</p>
'''

    pattern = r'(<!-- UNIQUE CONTENT FOR [^>]+ -->.*?<div style="max-width: \d+px; margin: 0 auto;">)(.*?)(</div>\s*</section>\s*<!-- END UNIQUE CONTENT -->)'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        if 'services are available throughout' in match.group(2):
            return content, False

        new_content = match.group(1) + match.group(2) + links_html + match.group(3)
        content = content[:match.start()] + new_content + content[match.end():]
        return content, True

    return content, False


def process_file(file_path):
    """Process a single file and add appropriate links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if no unique content section
    if '<!-- UNIQUE CONTENT FOR' not in content:
        return False

    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    modified = False

    # Neighborhood page: /ny/{neighborhood}/index.html
    if len(parts) >= 2 and parts[0] == 'ny' and parts[-1] == 'index.html':
        neighborhood_slug = parts[1]
        content, modified = add_neighborhood_links(content, neighborhood_slug)

    # Brand page: /brands/{brand}/index.html
    elif len(parts) >= 2 and parts[0] == 'brands' and parts[-1] == 'index.html':
        brand_slug = parts[1]
        content, modified = add_brand_links(content, brand_slug)

    # Appliance page: /appliances/{appliance}/index.html
    elif len(parts) >= 2 and parts[0] == 'appliances' and parts[-1] == 'index.html':
        appliance_slug = parts[1]
        content, modified = add_appliance_links(content, appliance_slug)

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} total pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if process_file(f):
            count += 1

    print(f"Added internal links to {count} pages")


if __name__ == "__main__":
    main()
