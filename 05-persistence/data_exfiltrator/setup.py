from setuptools import setup, find_packages

setup(
    name='data-exfiltrator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'data-exfiltrator=data_exfiltrator.main:main',
        ],
    },
    author='Your Name',
    description='Data exfiltration framework for post-exploitation',
    python_requires='>=3.7',
)