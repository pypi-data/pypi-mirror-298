from setuptools import setup, find_packages
import os

# Read the long description from the README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='py-sphviewer2',  # Package name
    version='1.0.0',  # Initial version number
    author='Alejandro Benitez-Llambay',
    author_email='alejandro.benitezllambay@unimib.it',
    description='A Python wrapper for SPH data rendering using the private smeshl C library.',
    long_description='',  # Make sure to have a README.md file in your directory
    long_description_content_type='text/markdown',
    url='https://alejandrobll.github.io/content/sphviewer2/',  # Replace with your project repository link
    packages=find_packages(),  # Automatically finds all packages within the directory
    include_package_data=True,  # Include package data specified in MANIFEST.in
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.0',
    ],
    project_urls={
        'Bug Tracker': 'https://alejandrobll.github.io/content/sphviewer2/',  # Replace with your repo issue tracker
    },
)
