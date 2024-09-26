from setuptools import setup, find_packages
import os

# Setup configuration
setup(
    name="applicare-ai",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "applicare-ai = utils.cli:cli",
        ]
    },
    author="applicare-ai",
    author_email="support@applicare-ai.com",
    description="Welcome to applicare-ai",
    long_description=open("readme.rst").read(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    extras_require={"dev": ["pytest", "wheel", "twine", "black", "setuptools"]},  # Include Cython for development
    dependency_links=[
        "git+ssh://git@github.com/infinity-sandbox/predictive-monitoring.git@14c737c247f36e3"
        "264deea5c4b9e0b0b940d17ba#egg=applicare_ai&subdirectory=server"
    ]
)