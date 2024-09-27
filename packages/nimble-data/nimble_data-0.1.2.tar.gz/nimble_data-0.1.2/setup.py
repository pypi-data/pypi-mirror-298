import setuptools
from pathlib import Path

VERSION = "0.1.2"

setuptools.setup(
    name="nimble_data",
    version=VERSION,
    description="Nimble SDK.",
    url="https://github.com/Nimbleway/sdk",
    project_urls={
        "Source Code": "https://github.com/Nimbleway/sdk",
    },
    author="Nimble",
    author_email="alonb@nimbleway.com",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
    ],
    #  requires Python 3.8
    python_requires=">=3.8",
    # Requirements
    #install_requires=INSTALL_REQUIRES,
    packages=["nimble_data"],
    long_description="Nimble SDK",
)