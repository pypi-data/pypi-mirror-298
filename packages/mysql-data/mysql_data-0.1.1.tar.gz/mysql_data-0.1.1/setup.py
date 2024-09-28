from setuptools import setup, find_packages

setup(
    name='mysql_data',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.3',
        'mysql-connector-python>=9.0.0',
    ]
)