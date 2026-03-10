#!/usr/bin/env python3
"""
Add unique content to ALL pages sitewide.
Handles: location pages, location+service pages, brand pages
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

# Location intros
LOCATION_INTROS = [
    "Known for its vibrant community, {location} residents deserve reliable appliance repair they can count on.",
    "As one of Manhattan's premier neighborhoods, {location} homeowners expect premium service.",
    "From luxury high-rises to classic walk-ups, {location} requires expert appliance technicians.",
    "Serving the heart of {location}, our technicians ensure fast response times for every call.",
    "{location} combines urban convenience with neighborhood charm - we keep appliances running smoothly.",
    "Whether you're in a {location} co-op, condo, or rental, we provide exceptional repair service.",
    "The busy lifestyle of {location} residents means you need repairs done right the first time.",
    "{location}'s mix of modern and pre-war buildings presents unique challenges we handle daily.",
    "We've served {location} families for years with honest, reliable appliance repair.",
    "From {location}'s tree-lined streets to bustling avenues, we're the trusted repair choice.",
]

# Service-specific intros
SERVICE_INTROS = {
    "washer": [
        "Our washer repair experts in {location} fix all brands - front load, top load, and stackable units.",
        "Washer not spinning or draining? Our {location} technicians diagnose and repair same-day.",
        "{location} residents trust us for fast, reliable washer repairs with genuine parts.",
    ],
    "dryer": [
        "Dryer repair in {location} - we fix heating issues, drum problems, and electrical faults.",
        "Our {location} dryer technicians handle gas and electric models from all major brands.",
        "Don't let a broken dryer pile up laundry - {location} same-day dryer repair available.",
    ],
    "refrigerator": [
        "Refrigerator repair in {location} - cooling issues, ice makers, and compressor service.",
        "Our {location} refrigerator experts service all brands including Sub-Zero and built-ins.",
        "Keep your food fresh with fast {location} refrigerator repair - same-day appointments.",
    ],
    "dishwasher": [
        "Dishwasher repair in {location} - leaks, drainage issues, and cleaning problems solved.",
        "Our {location} dishwasher technicians fix all brands quickly and affordably.",
        "{location} dishwasher not cleaning properly? We diagnose and repair same-day.",
    ],
    "oven": [
        "Oven repair in {location} - heating elements, igniters, and temperature issues fixed.",
        "Our {location} oven technicians service gas, electric, and convection models.",
        "From baking problems to complete failures, {location} oven repair done right.",
    ],
    "cooktop": [
        "Cooktop repair in {location} - burners, igniters, and electric elements serviced.",
        "Our {location} cooktop experts handle gas, electric, and induction models.",
        "{location} cooktop not heating? We diagnose and repair all brands same-day.",
    ],
    "microwave": [
        "Microwave repair in {location} - turntables, magnetrons, and control panels fixed.",
        "Our {location} microwave technicians service built-in and countertop units.",
        "{location} microwave not heating? Fast, affordable repair available today.",
    ],
    "default": [
        "Professional appliance repair in {location} - all brands and models serviced.",
        "Our {location} technicians arrive with parts for same-day repairs.",
        "Trusted appliance repair serving {location} with fast, reliable service.",
    ],
}

# Brand-specific intros
BRAND_INTROS = {
    "lg": "LG appliances feature advanced technology that requires specialized repair knowledge. Our certified technicians understand LG's ThinQ smart features, TurboWash systems, and InstaView technology.",
    "samsung": "Samsung appliances combine innovation with reliability. We're experts in Samsung's Family Hub refrigerators, FlexWash systems, and smart home integration.",
    "whirlpool": "Whirlpool has been a trusted American brand for generations. Our technicians know Whirlpool's reliable designs and can quickly diagnose any issue.",
    "ge": "GE appliances are found in homes across America. We service all GE models including Profile, Cafe, and Monogram lines.",
    "frigidaire": "Frigidaire offers dependable appliances at great value. Our technicians are experienced with all Frigidaire models and common repair needs.",
    "maytag": "Maytag is known for durability and performance. We repair all Maytag appliances with genuine parts for lasting results.",
    "kitchenaid": "KitchenAid appliances blend professional performance with home convenience. Our experts handle KitchenAid's premium features.",
    "bosch": "Bosch German engineering demands precision repair. Our technicians are trained on Bosch's quiet operation and efficiency features.",
    "thermador": "Thermador luxury appliances require expert care. We're certified to repair Thermador's professional-grade ranges and refrigeration.",
    "sub-zero": "Sub-Zero represents the pinnacle of refrigeration. Our specialists understand Sub-Zero's dual compressor systems and preservation technology.",
    "wolf": "Wolf professional cooking equipment demands expert service. We repair Wolf ranges, ovens, and cooktops to factory specifications.",
    "viking": "Viking professional appliances bring restaurant quality home. Our technicians are experienced with Viking's commercial-grade construction.",
    "miele": "Miele German engineering ensures longevity and performance. We service all Miele appliances with precision and care.",
    "default": "We service all major appliance brands with factory-trained expertise. Our technicians stay current on the latest models and repair techniques.",
}

FAQ_TEMPLATES = [
    [
        ("How quickly can you reach {location}?", "We typically arrive in {location} within 1-2 hours, often sooner."),
        ("Do you charge extra for {location} service?", "No hidden fees - our flat rate covers all of Manhattan including {location}."),
    ],
    [
        ("Are you licensed for {location}?", "Yes - fully licensed, insured, and background-checked for {location} service."),
        ("Do you offer weekend service in {location}?", "Absolutely - 7 days a week including holidays for {location} residents."),
    ],
    [
        ("What warranty do you offer in {location}?", "90-day parts and labor warranty on all {location} repairs."),
        ("Can you fix high-end appliances in {location}?", "Yes - we're certified for luxury brands commonly found in {location}."),
    ],
    [
        ("Is same-day repair available in {location}?", "Yes! Most {location} calls are completed same-day."),
        ("What payment methods do you accept?", "Credit cards, cash, and checks accepted for {location} service."),
    ],
]

def get_hash_index(text, num_options):
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % num_options

def format_name(slug):
    return slug.replace("-", " ").title()

def get_service_type(slug):
    if "washer" in slug: return "washer"
    if "dryer" in slug: return "dryer"
    if "refrigerator" in slug: return "refrigerator"
    if "dishwasher" in slug: return "dishwasher"
    if "oven" in slug: return "oven"
    if "cooktop" in slug: return "cooktop"
    if "microwave" in slug: return "microwave"
    return "default"

def generate_content(page_type, location=None, service=None, brand=None):
    """Generate unique content based on page type."""

    if page_type == "location":
        idx = get_hash_index(location, len(LOCATION_INTROS))
        intro = LOCATION_INTROS[idx].format(location=location)
        faq_idx = get_hash_index(location + "faq", len(FAQ_TEMPLATES))
        faqs = FAQ_TEMPLATES[faq_idx]

    elif page_type == "location_service":
        svc_type = get_service_type(service)
        svc_intros = SERVICE_INTROS.get(svc_type, SERVICE_INTROS["default"])
        idx = get_hash_index(location + service, len(svc_intros))
        intro = svc_intros[idx].format(location=location)
        faq_idx = get_hash_index(location + service, len(FAQ_TEMPLATES))
        faqs = FAQ_TEMPLATES[faq_idx]

    elif page_type == "brand":
        brand_key = brand.lower().replace(" ", "-").replace("_", "-")
        intro = BRAND_INTROS.get(brand_key, BRAND_INTROS["default"])
        faqs = []

    else:
        return None

    faq_html = ""
    for q, a in faqs:
        q_fmt = q.format(location=location) if location else q
        a_fmt = a.format(location=location) if location else a
        faq_html += f'''
        <div style="margin-bottom: 15px; padding: 12px; background: #f8f9fa; border-radius: 6px;">
            <strong style="color: var(--blue);">{q_fmt}</strong>
            <p style="margin: 8px 0 0 0; color: #555;">{a_fmt}</p>
        </div>'''

    title = location or brand or "Our Service"
    section = f'''
    <!-- UNIQUE CONTENT FOR {title.upper()} -->
    <section style="padding: 30px 20px; background: #fff;">
        <div style="max-width: 800px; margin: 0 auto;">
            <p style="font-size: 17px; line-height: 1.7; margin-bottom: 20px;">{intro}</p>
            {faq_html}
        </div>
    </section>
    <!-- END UNIQUE CONTENT -->
'''
    return section

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    if '<!-- UNIQUE CONTENT FOR' in content:
        return False

    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    if parts[-1] == 'index.html':
        parts = parts[:-1]

    if len(parts) == 0:
        return False

    # Determine page type
    if parts[0] == 'ny' and len(parts) == 2:
        page_type = "location"
        location = format_name(parts[1])
        unique_content = generate_content(page_type, location=location)

    elif parts[0] == 'ny' and len(parts) == 3:
        page_type = "location_service"
        location = format_name(parts[1])
        service = parts[2]
        unique_content = generate_content(page_type, location=location, service=service)

    elif parts[0] == 'brands' and len(parts) >= 2:
        page_type = "brand"
        brand = format_name(parts[1])
        unique_content = generate_content(page_type, brand=brand)

    else:
        return False

    if not unique_content:
        return False

    # Insert content
    if '</main>' in content:
        content = content.replace('</main>', unique_content + '</main>')
    elif '<footer' in content:
        content = re.sub(r'(<footer)', unique_content + r'\1', content, count=1)
    else:
        content = content.replace('</body>', unique_content + '</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} total pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if process_file(f):
            count += 1

    print(f"Added unique content to {count} pages")

if __name__ == "__main__":
    main()
