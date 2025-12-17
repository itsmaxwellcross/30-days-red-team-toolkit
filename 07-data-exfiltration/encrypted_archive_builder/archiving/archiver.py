"""
Archive creation and extraction
"""

import zipfile
import tarfile
from pathlib import Path

from config import SUPPORTED_FORMATS, ARCHIVE_FORMAT_INFO


class Archiver:
    """Handles archive creation and extraction"""
    
    def __init__(self):
        pass
    
    def create_zip(self, files_or_dirs, output_path):
        """
        Create ZIP archive
        
        Args:
            files_or_dirs (list): Files/directories to archive
            output_path (str): Output ZIP file path
            
        Returns:
            str: Path to created archive
        """
        print(f"[*] Creating ZIP archive: {output_path}")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in files_or_dirs:
                path = Path(item)
                
                if path.is_file():
                    zipf.write(path, path.name)
                    print(f"  [+] Added: {path.name}")
                
                elif path.is_dir():
                    for file_path in path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(path.parent)
                            zipf.write(file_path, arcname)
                            print(f"  [+] Added: {arcname}")
        
        print(f"[+] ZIP archive created: {output_path}")
        
        return output_path
    
    def create_tar(self, files_or_dirs, output_path, compression='gz'):
        """
        Create TAR archive
        
        Args:
            files_or_dirs (list): Files/directories to archive
            output_path (str): Output TAR file path
            compression (str): Compression type (gz, bz2, or None)
            
        Returns:
            str: Path to created archive
        """
        if compression == 'gz':
            mode = 'w:gz'
            print(f"[*] Creating TAR.GZ archive: {output_path}")
        elif compression == 'bz2':
            mode = 'w:bz2'
            print(f"[*] Creating TAR.BZ2 archive: {output_path}")
        else:
            mode = 'w'
            print(f"[*] Creating TAR archive: {output_path}")
        
        with tarfile.open(output_path, mode) as tar:
            for item in files_or_dirs:
                path = Path(item)
                
                if path.exists():
                    arcname = path.name
                    tar.add(path, arcname=arcname)
                    print(f"  [+] Added: {arcname}")
        
        print(f"[+] TAR archive created: {output_path}")
        
        return output_path
    
    def create_archive(self, files_or_dirs, output_path, format='zip'):
        """
        Create archive in specified format
        
        Args:
            files_or_dirs (list): Files/directories to archive
            output_path (str): Output file path
            format (str): Archive format (zip, tar.gz, tar.bz2, tar)
            
        Returns:
            str: Path to created archive
        """
        if format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}. Supported: {SUPPORTED_FORMATS}")
        
        # Ensure output has correct extension
        path = Path(output_path)
        expected_ext = ARCHIVE_FORMAT_INFO[format]['extension']
        
        if not output_path.endswith(expected_ext):
            output_path = str(path.with_suffix(expected_ext))
        
        if format == 'zip':
            return self.create_zip(files_or_dirs, output_path)
        
        elif format == 'tar.gz':
            return self.create_tar(files_or_dirs, output_path, compression='gz')
        
        elif format == 'tar.bz2':
            return self.create_tar(files_or_dirs, output_path, compression='bz2')
        
        elif format == 'tar':
            return self.create_tar(files_or_dirs, output_path, compression=None)
    
    def extract_zip(self, archive_path, output_dir):
        """
        Extract ZIP archive
        
        Args:
            archive_path (str): Path to ZIP file
            output_dir (str): Output directory
            
        Returns:
            str: Output directory path
        """
        print(f"[*] Extracting ZIP archive: {archive_path}")
        
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            zipf.extractall(output_dir)
            print(f"[+] Extracted {len(zipf.namelist())} file(s)")
        
        print(f"[+] Extraction complete: {output_dir}")
        
        return output_dir
    
    def extract_tar(self, archive_path, output_dir):
        """
        Extract TAR archive
        
        Args:
            archive_path (str): Path to TAR file
            output_dir (str): Output directory
            
        Returns:
            str: Output directory path
        """
        print(f"[*] Extracting TAR archive: {archive_path}")
        
        with tarfile.open(archive_path, 'r:*') as tar:
            tar.extractall(output_dir)
            print(f"[+] Extracted {len(tar.getmembers())} file(s)")
        
        print(f"[+] Extraction complete: {output_dir}")
        
        return output_dir
    
    def extract_archive(self, archive_path, output_dir):
        """
        Extract archive (auto-detect format)
        
        Args:
            archive_path (str): Path to archive
            output_dir (str): Output directory
            
        Returns:
            str: Output directory path
        """
        path = Path(archive_path)
        
        if path.suffix == '.zip':
            return self.extract_zip(archive_path, output_dir)
        
        elif path.suffix in ['.tar', '.gz', '.bz2'] or '.tar.' in path.name:
            return self.extract_tar(archive_path, output_dir)
        
        else:
            raise ValueError(f"Unknown archive format: {path.suffix}")
    
    def list_archive_contents(self, archive_path):
        """
        List contents of archive
        
        Args:
            archive_path (str): Path to archive
            
        Returns:
            list: List of file names in archive
        """
        path = Path(archive_path)
        
        if path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                return zipf.namelist()
        
        elif path.suffix in ['.tar', '.gz', '.bz2'] or '.tar.' in path.name:
            with tarfile.open(archive_path, 'r:*') as tar:
                return tar.getnames()
        
        else:
            raise ValueError(f"Unknown archive format: {path.suffix}")
    
    def get_archive_info(self, archive_path):
        """
        Get information about archive
        
        Args:
            archive_path (str): Path to archive
            
        Returns:
            dict: Archive information
        """
        path = Path(archive_path)
        
        if not path.exists():
            return None
        
        contents = self.list_archive_contents(archive_path)
        
        return {
            'path': str(path),
            'name': path.name,
            'format': path.suffix,
            'size': path.stat().st_size,
            'file_count': len(contents),
            'files': contents
        }