"""
Cloud C2 Core - Base S3 client functionality
"""

import sys
import boto3
from botocore.exceptions import ClientError


class CloudC2:
    """
    Cloud C2 Base Class
    Handles S3 bucket operations for command and control
    """
    
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region='us-east-1'):
        """
        Initialize Cloud C2
        
        Args:
            bucket_name (str): S3 bucket name
            aws_access_key (str): AWS access key ID
            aws_secret_key (str): AWS secret access key
            region (str): AWS region (default: us-east-1)
        """
        self.bucket_name = bucket_name
        self.region = region
        
        # Initialize S3 client
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        # Ensure bucket exists
        self.ensure_bucket()
        
        print(f"[+] Cloud C2 initialized")
        print(f"[+] Bucket: {bucket_name}")
        print(f"[+] Region: {region}")
    
    def ensure_bucket(self):
        """Ensure S3 bucket exists, create if necessary"""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"[+] Using existing bucket: {self.bucket_name}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == '404':
                # Bucket doesn't exist - create it
                self._create_bucket()
            elif error_code == '403':
                print(f"[-] Access denied to bucket: {self.bucket_name}")
                sys.exit(1)
            else:
                print(f"[-] Bucket error: {e}")
                sys.exit(1)
    
    def _create_bucket(self):
        """Create S3 bucket"""
        try:
            if self.region == 'us-east-1':
                # us-east-1 doesn't need LocationConstraint
                self.s3.create_bucket(Bucket=self.bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            print(f"[+] Created bucket: {self.bucket_name}")
        except ClientError as e:
            print(f"[-] Failed to create bucket: {e}")
            sys.exit(1)
    
    def upload_object(self, key, data, metadata=None):
        """
        Upload data to S3
        
        Args:
            key (str): S3 object key
            data (str|bytes): Data to upload
            metadata (dict): Optional metadata
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            kwargs = {
                'Bucket': self.bucket_name,
                'Key': key,
                'Body': data.encode() if isinstance(data, str) else data
            }
            
            if metadata:
                kwargs['Metadata'] = metadata
            
            self.s3.put_object(**kwargs)
            return True
        except ClientError as e:
            print(f"[-] Upload error: {e}")
            return False
    
    def download_object(self, key):
        """
        Download data from S3
        
        Args:
            key (str): S3 object key
        
        Returns:
            str: Downloaded data or None if not found
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read().decode()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            else:
                print(f"[-] Download error: {e}")
                return None
    
    def delete_object(self, key):
        """
        Delete object from S3
        
        Args:
            key (str): S3 object key
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            print(f"[-] Delete error: {e}")
            return False
    
    def list_objects(self, prefix='', max_keys=1000):
        """
        List objects in bucket
        
        Args:
            prefix (str): Filter by prefix
            max_keys (int): Maximum number of keys to return
        
        Returns:
            list: List of object keys
        """
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                return []
        except ClientError as e:
            print(f"[-] List error: {e}")
            return []
    
    def object_exists(self, key):
        """
        Check if object exists
        
        Args:
            key (str): S3 object key
        
        Returns:
            bool: True if exists, False otherwise
        """
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError:
            return False
    
    def get_object_metadata(self, key):
        """
        Get object metadata
        
        Args:
            key (str): S3 object key
        
        Returns:
            dict: Object metadata or None
        """
        try:
            response = self.s3.head_object(Bucket=self.bucket_name, Key=key)
            return {
                'size': response['ContentLength'],
                'last_modified': response['LastModified'],
                'metadata': response.get('Metadata', {})
            }
        except ClientError:
            return None
    
    def delete_all_objects(self, prefix=''):
        """
        Delete all objects with given prefix
        
        Args:
            prefix (str): Prefix filter
        
        Returns:
            int: Number of objects deleted
        """
        objects = self.list_objects(prefix=prefix)
        count = 0
        
        for key in objects:
            if self.delete_object(key):
                count += 1
        
        return count
    