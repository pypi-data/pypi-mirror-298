from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proitav-api-wrappers",
    version="1.3.2",
    packages=find_packages(),
    description="API Wrapper for ProITAV Products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Justin Faulk",
    author_email="jfaulk@proitav.us",
    url="https://github.com/jfaulk1434/proitav-api-wrappers",
    install_requires=[
        "pyserial",
        "pexpect",
        "telnetlib3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
