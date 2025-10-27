# Phishing Template Generator

Modular, extensible phishing template generator with personalized content based on reconnaissance data.

## Features

- **7 Template Types**: CEO fraud, security alerts, HR docs, vendor invoices, IT requests, collaboration, social media
- **Personalization**: Uses target data (name, role, company, tech stack)
- **Variants**: Generate multiple versions of each template
- **Extensible**: Easy to add new template types
- **Type-Safe**: Full type hints for better IDE support
- **Clean Architecture**: Separation of concerns, testable components

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from template_generator import TemplateGenerator, TargetData

# Create target data
target = TargetData(
    name="John Doe",
    email="john.doe@example.com",
    title="Senior Developer",
    department="Engineering",
    company_name="Example Corp",
    company_domain="example.com",
    technologies_used=["Office 365", "Slack", "AWS"]
)

# Generate templates
generator = TemplateGenerator(target)

# Get specific template
ceo_fraud = generator.generate('ceo_fraud')

# Get all templates
all_templates = generator.get_all_templates()

# Generate variants
variants = generator.generate_variants('security_alert', count=3)
```

## CLI Usage

```bash
# List available template types
python -m template_generator list

# Generate all templates
python -m template_generator generate target.json

# Generate specific template
python -m template_generator generate target.json ceo_fraud

# Show example
python -m template_generator example
```

## File Structure

```
template_generator/
├── core/              # Core logic
│   ├── generator.py   # Main orchestrator
│   └── target.py      # Target data model
├── templates/         # Template implementations
│   ├── base.py       # Base template class
│   ├── ceo_fraud.py  # CEO fraud templates
│   ├── security.py   # Security alerts
│   ├── hr.py         # HR documents
│   ├── vendor.py     # Vendor invoices
│   ├── it.py         # IT requests
│   ├── collaboration.py  # Collaboration
│   └── social_media.py   # Social media
├── utils/            # Utilities
└── config/           # Configuration
```

## Adding New Templates

1. Create new template class in `templates/`:

```python
from .base import BaseTemplate

class MyTemplate(BaseTemplate):
    def generate(self) -> dict:
        subject = f"Custom Subject for {self.target.name}"
        body = f"Custom body..."
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='my_template',
            urgency='medium'
        )
```

2. Register in `templates/__init__.py`
3. Add to `core/generator.py` templates dict

## Template Output Format

Each template returns:

```python
{
    'subject': 'Email subject line',
    'body': 'Email body with [TRACKING_LINK: text] placeholders',
    'template_type': 'template_identifier',
    'urgency': 'low|medium|high'
}
```

## Integration

```python
# With phishing framework
from phishing_framework import PhishingFramework
from template_generator import TemplateGenerator, TargetData

# Generate personalized template
target = TargetData(name="John", email="john@example.com")
generator = TemplateGenerator(target)
template = generator.generate('ceo_fraud')

# Use with phishing framework
framework = PhishingFramework()
framework.send_email(
    to=target.email,
    subject=template['subject'],
    body=template['body']
)
```

## Testing

```python
import unittest
from template_generator import TemplateGenerator, TargetData

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.target = TargetData(
            name="Test User",
            email="test@example.com"
        )
        self.generator = TemplateGenerator(self.target)
    
    def test_generate_ceo_fraud(self):
        template = self.generator.generate('ceo_fraud')
        self.assertEqual(template['template_type'], 'ceo_fraud')
        self.assertIn(self.target.name, template['body'])
```

## Security Notes

- Templates include placeholder `[TRACKING_LINK:]` for insertion of actual URLs
- Never hardcode malicious URLs in templates
- Use only for authorized security testing
- Sanitize all user input before using in templates

## License

MIT License - For authorized security testing only

---

**⚠️ Legal Notice**: This tool is for authorized penetration testing and security awareness training only. Unauthorized use is illegal.