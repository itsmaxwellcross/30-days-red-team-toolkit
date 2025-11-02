"""
from setuptools import setup, find_packages

setup(
    name='credential-harvester',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'credential-harvester=credential_harvester.main:main',
        ],
    },
    author='Your Name',
    description='Post-exploitation credential harvesting framework',
    python_requires='>=3.7',
)
"""