import codecs
import os
from setuptools import setup, find_packages

# Define the directory containing the setup script
here = os.path.abspath(os.path.dirname(__file__))

# Read the README.md file for the long_description
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

# Package metadata
VERSION = '0.0.13'
DESCRIPTION = 'Downstream analysis tool for spatial transcriptomics data, especially for data from HDSTDb'
LONG_DESCRIPTION = 'A package that allows you to download data from HDSTDb and perform downstream analysis on spatial transcriptomics data'

# Setup configuration
setup(
    name="process_hdst",
    version=VERSION,
    author="LabW",
    author_email="yiru.22@intl.zju.edu.cn",
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'anndata',
        'plotly',
        'matplotlib',
        'seaborn',
        'scanpy',
        'scipy',
        'squidpy',
    ],
    keywords=['python', 'spatial transcriptomics', 'database', 'bioinformatics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'process-hdst=process_HDST.cli:main'
        ]
    }
)