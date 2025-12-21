"""
Setup configuration for Windows Event Log Manipulation Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="windows-log-manipulation",
    version="1.0.0",
    author="Red Team Operations",
    description="Framework for Windows Event Log analysis and manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/windows-log-manipulation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No strict dependencies - uses standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "full": [
            # Optional production-grade EVTX parsing
            # "pyevtx>=20201107",
        ],
    },
    entry_points={
        "console_scripts": [
            "winlog-tool=windows_log_manipulation.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)