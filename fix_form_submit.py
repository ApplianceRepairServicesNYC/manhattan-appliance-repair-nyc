#!/usr/bin/env python3
"""
Update all subpage forms to show success modal like homepage.
"""

import re
from pathlib import Path

BASE_DIR = Path('/Users/globalaffiliate/manhattan-appliance-repair-nyc')

# Success modal HTML
SUCCESS_MODAL = '''
<!-- Success Modal -->
<div id="formModalOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9998;"></div>
<div id="formSuccessModal" style="display:none; position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:white; padding:40px; border-radius:12px; text-align:center; z-index:9999; max-width:400px; box-shadow:0 10px 40px rgba(0,0,0,0.3);">
<div style="font-size:50px; margin-bottom:20px;">✓</div>
<p id="formSuccessMessage" style="font-size:18px; line-height:1.6; color:#333;"><strong>Thank you!</strong><br><br>Your request has been sent.<br><br>We will contact you within 30 minutes.</p>
<button onclick="document.getElementById('formSuccessModal').style.display='none';document.getElementById('formModalOverlay').style.display='none';" style="margin-top:20px; padding:12px 30px; background:var(--blue,#003087); color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer;">Close</button>
</div>
'''

# AJAX form submission script
FORM_SCRIPT = '''
<script>
document.addEventListener('DOMContentLoaded', function() {
    var scheduleForm = document.getElementById('scheduleForm');
    if (scheduleForm && !scheduleForm.dataset.ajaxBound) {
        scheduleForm.dataset.ajaxBound = 'true';
        scheduleForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var formData = new FormData(scheduleForm);
            var email = formData.get('email') || '';

            fetch('https://formsubmit.co/ajax/insuranceappliance@gmail.com', {
                method: 'POST',
                body: formData
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                scheduleForm.reset();
                var msg = '<strong>Thank you!</strong><br><br>Your request has been sent.';
                if (email) {
                    msg += '<br><br>We will contact you at<br><strong>' + email + '</strong><br>within 30 minutes.';
                } else {
                    msg += '<br><br>We will contact you within 30 minutes.';
                }
                document.getElementById('formSuccessMessage').innerHTML = msg;
                document.getElementById('formSuccessModal').style.display = 'block';
                document.getElementById('formModalOverlay').style.display = 'block';
            })
            .catch(function(error) {
                alert('Failed to send. Please try again or call us.');
            });
        });
    }
});
</script>
'''

def fix_form(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return False

    # Skip if already has the success modal
    if 'formSuccessModal' in content:
        return False

    # Skip if no schedule form
    if 'id="scheduleForm"' not in content:
        return False

    # Skip homepage
    if file_path == BASE_DIR / 'index.html':
        return False

    modified = False

    # Change form from regular submit to AJAX
    # Remove action and method from form tag
    content = re.sub(
        r'<form id="scheduleForm" action="[^"]*" method="POST">',
        '<form id="scheduleForm">',
        content
    )

    # Add success modal before </body>
    if '</body>' in content:
        content = content.replace('</body>', SUCCESS_MODAL + '\n' + FORM_SCRIPT + '\n</body>')
        modified = True

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
        if fix_form(f):
            count += 1

    print(f"Updated form submission on {count} pages")


if __name__ == "__main__":
    main()
