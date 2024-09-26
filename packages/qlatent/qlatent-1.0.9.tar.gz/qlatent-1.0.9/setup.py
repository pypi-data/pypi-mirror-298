from setuptools import setup, find_packages
from pathlib import Path
from pkg_resources import parse_requirements

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
name="qlatent",
version="1.0.9",
description="A Python package for running psychometric on LLMs.",
packages=find_packages(),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: Apache Software License",
"Operating System :: OS Independent",
],
include_package_data=True,
python_requires=">=3.8",
install_requires=[
"numpy==1.24.4",
"pandas",
"seaborn",
"scipy",
"scikit-learn",
"transformers",
"pingouin",
"typeguard",
"datasets",
"evaluate",
"matplotlib",
"sentence_transformers",
],
long_description=long_description,
long_description_content_type='text/markdown',
url="https://github.com/cnai-lab/qlatent/",
project_urls={'Academic Article': 'https://openreview.net/pdf/026597881acf1899856edfa5147390a6a60bd3a8.pdf'},
)