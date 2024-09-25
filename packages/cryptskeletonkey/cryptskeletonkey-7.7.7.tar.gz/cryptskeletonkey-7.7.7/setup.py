# setup.py

from setuptools import setup, find_packages

setup(
    name="cryptskeletonkey",
    version="7.7.7",
    description="Generate mnemonic phrases and derive Ethereum, Bech32, P2PKH, and P2SH addresses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DeadManRiffs",
    author_email="your.email@example.com",
    url="https://github.com/deadmanriffs/cryptskeletonkey",  # Update this with your actual URL
    packages=find_packages(),
    install_requires=[
        'mnemonic',
        'bip32utils',
        'web3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
