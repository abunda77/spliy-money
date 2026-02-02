"""
Setup script untuk Money Splitter application
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="money-splitter",
    version="1.0.0",
    author="Money Splitter Team",
    description="Aplikasi untuk membagi uang menjadi beberapa bagian secara natural",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # tkinter is built-in
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "hypothesis>=6.0.0",
            "pytest-cov>=4.0.0",
        ],
        "dev": [
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "money-splitter=main:main",
        ],
    },
)