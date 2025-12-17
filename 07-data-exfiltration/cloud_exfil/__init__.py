#!/usr/bin/env python3
"""
Cloud Exfiltration Framework
Exfiltrate via AWS S3, Google Drive, Dropbox, OneDrive, Pastebin
"""

from .core import CloudExfiltrator
from .base_provider import BaseCloudProvider
from .aws_s3 import S3Provider
from .google_drive import GoogleDriveProvider
from .dropbox import DropboxProvider
from .onedrive import OneDriveProvider
from .pastebin import PastebinProvider

__version__ = '1.0.0'
__all__ = [
    'CloudExfiltrator',
    'BaseCloudProvider',
    'S3Provider',
    'GoogleDriveProvider',
    'DropboxProvider',
    'OneDriveProvider',
    'PastebinProvider'
]