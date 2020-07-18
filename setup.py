from distutils.core import setup
from setuptools import find_packages
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''


setup(
    name="text_toolkit",

    # Start with a small number and increase it with every change you make
    # https://semver.org
    version='1.0.0',
    # Packages to include into the distribution
    packages=find_packages(),

    # Short description of your library
    description='',

    # Long description of your library
    long_description=long_description,
    long_description_context_type='text/markdown',

    # Your name
    author='',

    # Your email
    author_email='ruxiz2005@gmail.com',

    # Either the link to your github or to your website
    url='https://github.com/ruxiz2020/text_toolkit',

    # Link from which the project can be downloaded
    download_url='',

    # List of keyword arguments
    keywords=[],

    # List of packages to install with this one
    install_requires=[],

    # https://pypi.org/classifiers/
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent", ],
    python_requires='>=3.6',
)
