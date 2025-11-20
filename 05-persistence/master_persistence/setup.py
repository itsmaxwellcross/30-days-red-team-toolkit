"""
Setup script for Master Persistence Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="master-persistence",
    version="1.0.0",
    author="Maxwell Cross",
    author_email="maxwell@redteam.lab",
    description="Master Windows Persistence Framework - Comprehensive persistence orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxwellcross/30-days-red-team",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses Windows built-ins
    ],
    entry_points={
        "console_scripts": [
            "master-persistence=main:main",
        ],
    },
)