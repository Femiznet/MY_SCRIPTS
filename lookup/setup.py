"""
Setup configuration for the lookup package.

Installs the 'lookup' command globally, runnable from anywhere.
"""

import re
from pathlib import Path
from setuptools import setup

# Read version from lookup.py
version_file = Path(__file__).parent / "lookup.py"
version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read_text(), re.MULTILINE)
if version_match:
    version = version_match.group(1)
else:
    version = "1.0.0"

setup(
    name="lookup",
    version=version,
    description="Cross-platform CLI utility to lookup files/directories by pattern, with open/delete actions",
    author="Femiznet",
    author_email="femiznet.dev@gmail.com",
    url="https://github.com/femiznet/yourusername/lookup",
    
    py_modules=["lookup"],
    
    # Create the 'lookup' command globally available
    entry_points={
        "console_scripts": [
            "lookup=lookup:main",
        ],
    },
    
    python_requires=">=3.10",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
)
