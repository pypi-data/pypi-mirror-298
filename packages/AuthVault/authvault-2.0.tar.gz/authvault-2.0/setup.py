from setuptools import setup, find_packages
from pathlib import Path

# Read the README.md file with the correct encoding
long_description = Path("README.md").read_text(encoding='utf-8')

setup(
    name="AuthVault",
    version='2.0',  # Package version
    packages=find_packages(),  # Automatically find the package directory
    install_requires=[
        'requests',  # External dependencies
    ],  # You can omit or leave blank if not using a repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify that the long description is in Markdown
    author="QSXD",
    author_email="n3v1n22@gmail.com",
    url="",

)
