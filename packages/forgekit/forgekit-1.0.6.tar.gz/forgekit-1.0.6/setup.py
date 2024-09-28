from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="forgekit",
    version="1.0.6",
    description="A collection of handy tools for data handling, visualization, and reporting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="0xMarc",
    project_urls={
        "Source": "https://github.com/0xMarcio/forgekit",
        "Bug Tracker": "https://github.com/0xMarcio/forgekit/issues",
    },
    author_email="marc@codepwn.win",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.3",
        "numpy>=2.1.1",
        "matplotlib>=3.9.2",
        "plotly>=5.24.1",
        "scikit-learn>=1.5.2",
        "tabulate2>=1.9.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
