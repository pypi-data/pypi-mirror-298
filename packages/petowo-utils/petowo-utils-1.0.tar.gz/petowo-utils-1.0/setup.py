from setuptools import setup, find_packages
from utils import __version__

setup(
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    name='petowo-utils',
    version=__version__,
    url='https://github.com/fleshbound/petowo-utils',
    author='Valeria Avdeykina',
    author_email='avdeykina@icloud.com',

    packages=find_packages(),

    install_requires=[
        'logging'
    ]
)

