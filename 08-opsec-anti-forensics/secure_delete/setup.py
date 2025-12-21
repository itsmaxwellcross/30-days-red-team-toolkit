"""
Setup configuration for Secure File Deletion Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="secure-delete",
    version="1.0.0",
    author="Red Team Operations",
    description="Secure file deletion and forensic artifact cleanup framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/secure-delete",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No strict dependencies - uses standard library
    ],
    extras_require={
        "windows": [
            "pywin32>=305",  # For Windows registry operations
        ],
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "secure-delete=secure_delete.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)