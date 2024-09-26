from setuptools import setup, find_packages
from tech import __version__

setup(
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    name='petowo-tech',
    version=__version__,
    url='https://github.com/fleshbound/petowo-tech',
    author='Valeria Avdeykina',
    author_email='avdeykina@icloud.com',

    packages=find_packages(),

    install_requires=[
        'typing',
        'pydantic==2.7.1',
        'logging',
        'datetime',
        'petowo-core'
    ]
)
