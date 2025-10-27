"""
Vendor invoice and payment templates
"""
import random
from datetime import datetime, timedelta
from .base import BaseTemplate

class VendorInvoiceTemplate(BaseTemplate):
    """Vendor invoice and payment request templates"""
    
    def generate(self) -> dict:
        """Generate vendor invoice template"""
        vendors = ['Adobe', 'Microsoft', 'AWS', 'Salesforce', 'Zoom', 'Slack', 'DocuSign']
        vendor = random.choice(vendors)
        amount = random.randint(500, 5000)
        invoice_num = random.randint(10000, 99999)
        
        subject = f"Invoice #{invoice_num} - Payment Due"
        
        body = f'''
Dear {self.target.name},

This is a payment reminder for {vendor} services.

Invoice Number: INV-{invoice_num}
Amount Due: ${amount:,}.00
Due Date: {(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')}

[TRACKING_LINK: View Invoice and Pay Online]

Late payments may result in service interruption.

If you have already processed this payment, please disregard this notice.

Thank you,
{vendor} Billing Department
billing@{vendor.lower()}.com
'''
        
        return self._format_template(
            subject=subject,
            body=body,
            template_type='vendor_invoice',
            urgency='medium'
        )