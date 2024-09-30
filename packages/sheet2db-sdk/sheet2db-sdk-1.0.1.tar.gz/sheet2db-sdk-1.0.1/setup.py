from setuptools import setup, find_packages

setup(
    name='sheet2db-sdk',
    version='1.0.1',
    description='A python library to interact with Google Sheets using sheet2db api',
    author='Sheet2DB',
    packages=find_packages(),
    url="https://sheet2db.com",
    author_email="support@sheet2db.com",
    keywords="sheet2db, google sheets, python, sdk",
    project_urls={  # Optional
        "Home Page": "https://sheet2db.com",
        "Documentation": "https://sheet2db.com/docs/sdks/python",
    },
    install_requires=[
        'requests'
    ]
)