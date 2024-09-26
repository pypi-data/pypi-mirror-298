#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup
from nes import __version__


# Get the version number from the relevant file
version = __version__

with open("README.md", "r") as f:
    long_description = f.read()


REQUIREMENTS = {
    'install': [
        'geopandas',
        'rtree>=0.9.0',
        'pandas',
        'netcdf4',
        'numpy',
        'pyproj',
        'setuptools',
        'scipy',
        'filelock',
        'eccodes',
        'mpi4py-mpich',
        'shapely',
        'python-dateutil'
    ],
    'setup': [
        'setuptools_scm',
    ],
}


setup(
    name='NES',
    # license='',
    # platforms=['GNU/Linux Debian'],
    version=version,
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Carles Tena Medina, Alba Vilanova Cortezon",
    author_email='carles.tena@bsc.es, alba.vilanova@bsc.es',
    url='https://earth.bsc.es/gitlab/es/NES',

    keywords=['Python', 'NetCDF4', 'Grib2', 'Earth'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science"
    ],
    package_data={'': [
        'README.md',
        'CHANGELOG.rst',
        'LICENSE',
    ]
    },
    setup_requires=REQUIREMENTS['setup'],
    install_requires=REQUIREMENTS['install']
)
