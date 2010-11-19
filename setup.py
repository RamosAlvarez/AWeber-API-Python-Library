from setuptools import setup, find_packages

setup(
    name='aweber_api',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    include_package_data=True
)

