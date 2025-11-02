"""
from setuptools import setup, find_packages

setup(
    name='network-discovery',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'netifaces>=0.11.0',  # Optional: better interface detection
    ],
    entry_points={
        'console_scripts': [
            'network-discovery=network_discovery.main:main',
        ],
    },
    author='Your Name',
    description='Network discovery and lateral movement reconnaissance framework',
    python_requires='>=3.7',
)
"""