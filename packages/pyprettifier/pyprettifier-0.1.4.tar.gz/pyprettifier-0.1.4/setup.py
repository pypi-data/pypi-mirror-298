from setuptools import setup
from setuptools.command.install import install
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="pyprettifier",
    version="0.1.4",
    packages=["pyprettifier"],
    description="A simple Python utility to improve python output from simple string.",
    long_description=long_description,
    long_description_content_type='text/markdown',  
    author="Sandra Gutierrez",
    author_email="help@pyprettifier.com",
    install_requires=[
        "requests"
    ],
    python_requires='>=3.6'
)
