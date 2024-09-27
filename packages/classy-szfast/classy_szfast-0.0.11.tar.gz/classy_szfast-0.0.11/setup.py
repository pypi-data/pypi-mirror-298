from setuptools import setup, find_packages
import os
import sys
import shutil


# Setup configuration
setup(
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
    ],
    name="classy_szfast",
    version="0.0.11",
    description="Python package for fast class_sz",
    # long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=find_packages(include=["classy_szfast"]),
    package_dir={},
    package_data={},
    author="Boris Bolliet, Ola Kusiak",
    author_email="bb667@cam.ac.uk, akk2175@columbia.edu",
    url='https://github.com/CLASS-SZ/classy_szfast',
    download_url='https://github.com/CLASS-SZ/classy_szfast',
    
    install_requires=["setuptools", "wheel", "numpy>=1.19.0", "Cython>=0.29.21", "tensorflow==2.13.0", "tensorflow-probability==0.21.0", "cosmopower", "mcfit"],
)

