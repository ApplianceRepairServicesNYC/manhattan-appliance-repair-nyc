#!/usr/bin/env python3
"""
Add contact form to all subpages that are missing it.
"""

import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

CONTACT_FORM_HTML = '''
<!-- SCHEDULE FORM SECTION -->
<section id="scheduleSection" style="padding: 60px 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
<div class="container" style="max-width: 700px;">
<div style="text-align: center; margin-bottom: 20px;">
<h2 style="color: var(--blue); margin-bottom: 10px;">Schedule Your Repair</h2>
<p style="color: #666;">Complete the form below and we'll contact you within 30 minutes.</p>
</div>
<div class="schedule-form-container active" id="scheduleFormContainer" style="background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
<form id="scheduleForm" action="https://formsubmit.co/insuranceappliance@gmail.com" method="POST">
<input type="hidden" name="_subject" value="New Repair Request from Website">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_template" value="table">
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
<div>
<label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Name *</label>
<input type="text" name="name" placeholder="Your Name" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box;">
</div>
<div>
<label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Phone *</label>
<input type="tel" name="phone" placeholder="Your Phone" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box;">
</div>
</div>
<div style="margin-bottom: 15px;">
<label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email *</label>
<input type="email" name="email" placeholder="Your Email" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box;">
</div>
<div style="margin-bottom: 15px;">
<label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Appliance Type *</label>
<select name="appliance" required style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box;">
<option value="" disabled selected>Select Appliance...</option>
<option value="Washer">Washer</option>
<option value="Dryer">Dryer</option>
<option value="Refrigerator">Refrigerator</option>
<option value="Dishwasher">Dishwasher</option>
<option value="Oven/Range">Oven/Range</option>
<option value="Cooktop">Cooktop</option>
<option value="Microwave">Microwave</option>
<option value="Other">Other</option>
</select>
</div>
<div style="margin-bottom: 20px;">
<label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Issue Description</label>
<textarea name="message" placeholder="Briefly describe the problem..." rows="3" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box; resize: vertical;"></textarea>
</div>
<button type="submit" style="width: 100%; padding: 15px; background: var(--red, #e41e26); color: white; border: none; border-radius: 6px; font-size: 18px; font-weight: 700; cursor: pointer; transition: background 0.3s;">Schedule Repair</button>
</form>
</div>
</div>
</section>
<!-- END SCHEDULE FORM SECTION -->
'''

SCROLL_JS = '''
<script>
// Schedule button scroll functionality
document.addEventListener('DOMContentLoaded', function() {
    var scheduleBtn = document.getElementById('heroScheduleBtn');
    if (scheduleBtn) {
        scheduleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            var formSection = document.getElementById('scheduleSection');
            if (formSection) {
                formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    }
    // Also handle any links with href="#contact" or "#schedule"
    document.querySelectorAll('a[href="#contact"], a[href="#schedule"], a[href="#scheduleSection"]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var formSection = document.getElementById('scheduleSection');
            if (formSection) {
                formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
</script>
'''

def add_contact_form(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already has schedule form section
    if 'id="scheduleSection"' in content or 'SCHEDULE FORM SECTION' in content:
        return False

    # Skip homepage (it already has a form)
    if file_path == BASE_DIR / 'index.html':
        return False

    modified = False

    # Add form before footer or before </body>
    if '<footer' in content:
        content = re.sub(r'(<footer)', CONTACT_FORM_HTML + r'\n\1', content, count=1)
        modified = True
    elif '</body>' in content:
        content = content.replace('</body>', CONTACT_FORM_HTML + '\n</body>')
        modified = True

    # Add scroll JS before </body>
    if modified and SCROLL_JS.strip() not in content:
        content = content.replace('</body>', SCROLL_JS + '\n</body>')

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    html_files = list(BASE_DIR.rglob('index.html'))
    print(f"Found {len(html_files)} pages")

    count = 0
    for f in html_files:
        if 'assets' in str(f) or 'sitemap' in str(f):
            continue
        if add_contact_form(f):
            count += 1

    print(f"Added contact form to {count} pages")


if __name__ == "__main__":
    main()
