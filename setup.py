from setuptools import setup, find_packages

setup(
    name="unifiedlogger",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Tosin Omisore",
    author_email="omisoretosin@yahoo.com",
    description="A unified logging package with support for colored and JSON output",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/unifiedlogger",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 