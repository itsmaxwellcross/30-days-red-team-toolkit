"""
Configuration settings
"""
import os

class Settings:
    """Global configuration for attachment weaponizer"""
    
    # Output directory
    DEFAULT_OUTPUT_DIR = "weaponized_attachments"
    
    # ZIP settings
    DEFAULT_ZIP_PASSWORD_LENGTH = 8
    ZIP_COMPRESSION_LEVEL = 9
    
    # Supported file types
    OFFICE_EXTENSIONS = ['.docm', '.xlsm', '.pptm', '.docx', '.xlsx']
    ARCHIVE_EXTENSIONS = ['.zip', '.iso', '.img']
    EXECUTABLE_EXTENSIONS = ['.exe', '.dll', '.scr', '.com', '.bat', '.cmd']
    
    # HTML smuggling settings
    HTML_SMUGGLING_DELAY = 1000  # milliseconds
    
    # LNK settings
    LNK_WINDOW_STYLES = {
        'hidden': 0,
        'normal': 1,
        'minimized': 7
    }
    
    # Macro templates
    MACRO_AUTO_OPEN_FUNCTIONS = [
        'Auto_Open',
        'Document_Open', 
        'Workbook_Open',
        'AutoOpen'
    ]
    
    # Safety settings
    REQUIRE_CONFIRMATION = True  # Confirm before creating attachments
    LOG_CREATION = True  # Log all created attachments
    
    # File size limits (bytes)
    MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB
    MAX_EMBEDDED_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10 MB for HTML smuggling