"""
from setuptools import setup, find_packages

setup(
    name='situational-awareness',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'situational-awareness=situational_awareness.main:main',
        ],
    },
    author='Your Name',
    description='Post-exploitation enumeration framework',
    python_requires='>=3.7',
)
"""