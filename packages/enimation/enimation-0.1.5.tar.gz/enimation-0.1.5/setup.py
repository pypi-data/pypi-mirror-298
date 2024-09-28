from setuptools import setup, find_packages
import os

# Load the README.md content
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='enimation',
    version='0.1.5',
    packages=find_packages(),
    description='A customizable loading tool',
    long_description=long_description,  # Use README.md content here
    long_description_content_type='text/markdown',  # Specify markdown format
    author='Hasanfq',
    author_email='hasanfq818@gmail.com',
    url='https://github.com/Kamanati/enimation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
) 
