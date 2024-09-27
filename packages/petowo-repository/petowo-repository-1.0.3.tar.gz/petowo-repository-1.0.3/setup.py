from setuptools import setup, find_packages
from repository import __version__

setup(
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
    name='petowo-repository',
    version=__version__,
    url='https://github.com/fleshbound/petowo-repository',
    author='Valeria Avdeykina',
    author_email='avdeykina@icloud.com',

    packages=find_packages(),

    install_requires=[
        'typing',
        'pydantic==2.7.1',
        'logging',
        'datetime',
        'dataclasses',
        'sqlalchemy',
        'psycopg2',
        'petowo-core',
    ]
)

