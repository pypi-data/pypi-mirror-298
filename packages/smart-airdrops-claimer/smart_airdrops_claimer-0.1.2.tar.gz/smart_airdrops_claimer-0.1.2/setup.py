from setuptools import setup, find_packages

setup(
    name="smart-airdrops-claimer",
    version="0.1.2",
    description="A package for airdrop automation.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Hoki Receh",
    author_email="ads.hokireceh@gmail.com",
    url="https://github.com/smartairdrops/smart-airdrops-claimer",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "requests",
        "brotli",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
