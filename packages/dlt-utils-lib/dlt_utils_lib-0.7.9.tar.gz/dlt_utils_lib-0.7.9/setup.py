from setuptools import setup, find_packages

setup(
    name='dlt_utils_lib',
    version='0.7.9',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'delta-spark',
    ],
)