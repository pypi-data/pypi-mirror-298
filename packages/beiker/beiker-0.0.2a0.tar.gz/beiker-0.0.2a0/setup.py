from setuptools import setup, find_packages

setup(
    name='beiker',
    version='0.0.2a',
    author='tarantella110',
    author_email='beiker110@126.com',
    description='developed for electronic archive sort',
    packages=find_packages(),
    install_requires=[
    'pandas',
    'mysql-connector-python',
    'pillow' ,
    'openpyxl',
    'PySide6'
],
)