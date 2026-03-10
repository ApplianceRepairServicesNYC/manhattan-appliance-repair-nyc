#!/usr/bin/env python3
"""
Add unique content to each location page to avoid duplicate content issues.
Adds: unique neighborhood descriptions, varied service text, local FAQs.
"""

import re
import hashlib
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

# Neighborhood descriptions - unique per location
NEIGHBORHOOD_INTROS = [
    "Known for its vibrant community and historic brownstones, {location} residents deserve reliable appliance repair they can count on.",
    "As one of Manhattan's most sought-after neighborhoods, {location} homeowners expect premium service - and that's exactly what we deliver.",
    "From luxury high-rises to classic walk-ups, {location} has diverse housing that requires expert appliance technicians who understand every setup.",
    "Serving the heart of {location}, our technicians navigate the neighborhood daily, ensuring fast response times for every service call.",
    "{location} combines urban convenience with neighborhood charm - and we're proud to keep your home appliances running smoothly.",
    "Whether you're in a {location} co-op, condo, or rental, our certified technicians provide the same exceptional repair service.",
    "The busy lifestyle of {location} residents means you need appliance repairs done right the first time - that's our guarantee.",
    "{location}'s mix of modern and pre-war buildings presents unique appliance challenges our experienced team handles daily.",
    "We've served {location} families for years, building a reputation for honest, reliable appliance repair service.",
    "From {location}'s tree-lined streets to its bustling avenues, we're the neighborhood's trusted appliance repair choice.",
]

# Service variations
SERVICE_INTROS = [
    "Our factory-trained technicians arrive with fully-stocked vehicles, ready to diagnose and repair your appliances on the spot.",
    "We combine decades of experience with cutting-edge diagnostic tools to get your appliances working like new.",
    "Same-day appointments available because we know a broken appliance disrupts your entire household routine.",
    "Transparent pricing, no hidden fees - we provide upfront quotes before any work begins.",
    "Licensed, bonded, and insured technicians who treat your home with the respect it deserves.",
    "We repair all major brands and stand behind our work with a satisfaction guarantee.",
    "Emergency repairs available - because appliance breakdowns don't wait for convenient timing.",
    "Our technicians undergo continuous training to stay current with the latest appliance technologies.",
    "Family-owned service means you'll speak with real people who care about solving your problem.",
    "We stock genuine manufacturer parts to ensure lasting repairs that extend your appliance's life.",
]

# Unique FAQs per location (rotated based on hash)
FAQ_SETS = [
    [
        ("How quickly can you reach {location}?", "Our technicians are strategically located throughout Manhattan. We typically arrive in {location} within 1-2 hours of your call, often sooner."),
        ("Do you charge extra for {location} service calls?", "No. Our flat diagnostic fee covers all of Manhattan including {location}. No surprise travel charges."),
        ("What appliance brands do you repair in {location}?", "We service all major brands - Samsung, LG, Whirlpool, GE, Sub-Zero, Viking, Thermador, Bosch, Miele, and more."),
    ],
    [
        ("Are your technicians licensed to work in {location}?", "Yes. All our technicians are fully licensed, insured, and background-checked to work in {location} and throughout NYC."),
        ("Do you offer weekend appointments in {location}?", "Absolutely. We offer 7-day service including weekends and holidays for {location} residents."),
        ("What's your warranty on repairs in {location}?", "All repairs come with a 90-day parts and labor warranty, giving {location} customers peace of mind."),
    ],
    [
        ("Can you repair high-end appliances in {location}?", "Yes. Our technicians are certified to repair luxury brands like Sub-Zero, Wolf, Viking, and Thermador commonly found in {location} homes."),
        ("Do you service apartment buildings in {location}?", "We regularly service apartments, condos, and co-ops throughout {location}. We're familiar with building access procedures."),
        ("What payment methods do you accept in {location}?", "We accept all major credit cards, cash, and checks. Payment is due upon completion of your {location} service call."),
    ],
    [
        ("How do I schedule a repair in {location}?", "Call us or book online. We'll confirm a convenient time window for your {location} appointment, usually same-day or next-day."),
        ("What if you can't fix my appliance in {location}?", "If a repair isn't cost-effective, we'll advise you honestly. You'll only pay the diagnostic fee, not a full repair charge."),
        ("Do {location} customers get priority service?", "All Manhattan customers receive the same fast, professional service. {location} is well within our primary coverage area."),
    ],
    [
        ("Is same-day repair available in {location}?", "Yes! Most {location} repair calls are completed same-day. Call before noon for best availability."),
        ("Do you haul away old appliances in {location}?", "We focus on repairs, but can recommend reliable {location} appliance removal services if needed."),
        ("What areas near {location} do you also cover?", "We serve all of Manhattan. Neighbors of {location} receive the same fast response times."),
    ],
]

def get_hash_index(location, num_options):
    """Get consistent index based on location name."""
    hash_val = int(hashlib.md5(location.encode()).hexdigest(), 16)
    return hash_val % num_options

def format_location(slug):
    """Convert slug to proper name."""
    return slug.replace("-", " ").title()

def generate_unique_section(location):
    """Generate unique content section for a location."""
    idx1 = get_hash_index(location + "intro", len(NEIGHBORHOOD_INTROS))
    idx2 = get_hash_index(location + "service", len(SERVICE_INTROS))
    idx3 = get_hash_index(location + "faq", len(FAQ_SETS))

    neighborhood_intro = NEIGHBORHOOD_INTROS[idx1].format(location=location)
    service_intro = SERVICE_INTROS[idx2].format(location=location)
    faqs = FAQ_SETS[idx3]

    faq_html = ""
    for q, a in faqs:
        q_formatted = q.format(location=location)
        a_formatted = a.format(location=location)
        faq_html += f'''
        <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <h4 style="margin: 0 0 10px 0; color: var(--blue);">{q_formatted}</h4>
            <p style="margin: 0; color: #555;">{a_formatted}</p>
        </div>'''

    unique_section = f'''
    <!-- UNIQUE CONTENT FOR {location.upper()} -->
    <section style="padding: 40px 20px; background: #fff;">
        <div style="max-width: 900px; margin: 0 auto;">
            <h2 style="text-align: center; color: var(--blue); margin-bottom: 30px;">Why {location} Chooses Us</h2>
            <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px;">{neighborhood_intro}</p>
            <p style="font-size: 18px; line-height: 1.8; margin-bottom: 30px;">{service_intro}</p>

            <h3 style="color: var(--blue); margin: 30px 0 20px;">Frequently Asked Questions - {location}</h3>
            {faq_html}
        </div>
    </section>
    <!-- END UNIQUE CONTENT -->
'''
    return unique_section

def add_unique_content(file_path):
    """Add unique content section to a page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already has unique content
    if '<!-- UNIQUE CONTENT FOR' in content:
        return False

    # Get location from path
    rel_path = file_path.relative_to(BASE_DIR)
    parts = list(rel_path.parts)

    if len(parts) < 2 or parts[0] != 'ny':
        return False

    # Only process main location pages (not sublevel)
    if len(parts) > 3:
        return False

    location = format_location(parts[1])
    unique_section = generate_unique_section(location)

    # Insert before closing </main> or before footer
    if '</main>' in content:
        content = content.replace('</main>', unique_section + '</main>')
    elif '<footer' in content:
        content = re.sub(r'(<footer)', unique_section + r'\1', content, count=1)
    else:
        # Insert before </body>
        content = content.replace('</body>', unique_section + '</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    ny_dir = BASE_DIR / 'ny'
    count = 0

    # Process only main location pages (ny/location/index.html)
    for loc_dir in ny_dir.iterdir():
        if loc_dir.is_dir():
            index_file = loc_dir / 'index.html'
            if index_file.exists():
                if add_unique_content(index_file):
                    count += 1

    print(f"Added unique content to {count} Manhattan location pages")

if __name__ == "__main__":
    main()
