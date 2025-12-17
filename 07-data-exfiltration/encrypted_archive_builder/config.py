"""
Configuration and constants for Encrypted Archive Builder
"""

# Encryption settings
ENCRYPTION_ALGORITHM = 'AES-256-CBC'
KEY_DERIVATION_ITERATIONS = 100000
KEY_LENGTH = 32  # 256 bits
SALT_LENGTH = 16  # 128 bits
IV_LENGTH = 16   # 128 bits
BLOCK_SIZE = 16  # AES block size

# Archive formats
SUPPORTED_FORMATS = ['zip', 'tar.gz', 'tar.bz2', 'tar']

ARCHIVE_FORMAT_INFO = {
    'zip': {
        'name': 'ZIP Archive',
        'extension': '.zip',
        'compression': 'DEFLATE',
        'speed': 'Fast',
        'ratio': 'Good'
    },
    'tar.gz': {
        'name': 'TAR with GZIP',
        'extension': '.tar.gz',
        'compression': 'GZIP',
        'speed': 'Fast',
        'ratio': 'Good'
    },
    'tar.bz2': {
        'name': 'TAR with BZIP2',
        'extension': '.tar.bz2',
        'compression': 'BZIP2',
        'speed': 'Slow',
        'ratio': 'Better'
    },
    'tar': {
        'name': 'TAR (no compression)',
        'extension': '.tar',
        'compression': 'None',
        'speed': 'Very Fast',
        'ratio': 'None'
    }
}

# Filename obfuscation templates
INNOCENT_FILENAME_TEMPLATES = [
    'meeting_notes_{date}.docx',
    'quarterly_report_{date}.xlsx',
    'presentation_{date}.pptx',
    'project_update_{date}.pdf',
    'team_photo_{date}.jpg',
    'budget_analysis_{date}.xlsx',
    'training_materials_{date}.pdf',
    'system_backup_{date}.zip',
    'conference_slides_{date}.pptx',
    'client_proposal_{date}.docx',
    'performance_review_{date}.pdf',
    'invoice_{date}.pdf',
    'contract_{date}.docx',
    'whitepaper_{date}.pdf',
    'research_data_{date}.xlsx'
]

# File extensions by category
DOCUMENT_EXTENSIONS = ['.docx', '.pdf', '.xlsx', '.pptx', '.txt']
IMAGE_EXTENSIONS = ['.jpg', '.png', '.gif', '.bmp']
ARCHIVE_EXTENSIONS = ['.zip', '.tar', '.gz', '.bz2']
DATA_EXTENSIONS = ['.csv', '.json', '.xml', '.db']

# Output settings
DEFAULT_OUTPUT_DIR = './encrypted_archives'
DEFAULT_CHUNK_SIZE = 64 * 1024  # 64KB chunks for processing

# Security settings
MINIMUM_PASSWORD_LENGTH = 8
RECOMMENDED_PASSWORD_LENGTH = 16

# Metadata
ENCRYPTED_FILE_MAGIC = b'ENCR'  # Magic bytes to identify encrypted files
ENCRYPTED_FILE_VERSION = 1