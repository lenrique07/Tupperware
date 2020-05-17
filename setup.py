from distutils.core import setup
from setuptools import find_packages

requires = ['tornado', 'sqlalchemy', 'configparser', 'schedule']

setup(
    name='Proyecto Banco Ganadero',
    version='1',
    packages=find_packages(),
    url='',
    license='Licence',
    author='Berthy Vargas Villarreal',
    author_email='berthy.v2@gmail.com',
    description='Server Base on Tornado framework',
    install_requires=requires
)