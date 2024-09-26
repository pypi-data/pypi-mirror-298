# ------------------------------------------------------------
# Filename: setup.py
# Description: Setup script for the contswi tool.
# Author: Gabor Puskas
# Email: pg@0r.hu
# Date: 2024-09-24
# Version: 0.1
# Dependencies: setuptools, kubectl
# Usage: Run this file to package and install the contswi CLI tool.
# ------------------------------------------------------------
from setuptools import setup, find_packages

setup(
    name='contswi',
    version='0.1.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'contswi = contswi.cli:main',
        ],
    },
    description="A simple kubectl context switcher cli tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Savalinn/contswi',  # ide jön a GitHub repo link
    author='Gabor Puskas',
    author_email='pg@0r.hu',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.7',
)
