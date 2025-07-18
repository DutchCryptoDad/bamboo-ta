from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.9.8"
DESCRIPTION = "TA library for Pandas"

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="bamboo-ta",
    version=VERSION,
    author="DutchCryptoDad (DCD)",
    author_email="<dutchcryptodad@gmail.com>",
    url="https://github.com/DutchCryptoDad/bamboo-ta",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=[
        "python",
        "pandas",
        "numpy",
        "trading",
        "indicator",
        "technical analysis",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",  # see https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=["pandas", "numpy"],
    extras_require={
        "def": ["pytest", "twine"],
    },
    python_requres=">=3.10",
)
