"""
Setup script for Registry Persistence Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="registry-persistence",
    version="1.0.0",
    author="Maxwell Cross",
    author_email="",
    description="Windows Registry Persistence Framework - Educational Use Only",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/registry-persistence",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
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
    entry_points={
        'console_scripts': [
            'registry-persistence=main:main',
        ],
    },
    install_requires=[
        # No external dependencies required
    ],
)