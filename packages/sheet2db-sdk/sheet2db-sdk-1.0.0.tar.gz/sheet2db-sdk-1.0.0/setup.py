from setuptools import setup, find_packages

setup(
    name='sheet2db-sdk',
    version='1.0.0',
    description='A python library to interact with Google Sheets using sheet2db api',
    author='Sheet2DB',
    packages=find_packages(),
    install_requires=[
        'requests'
    ]
)