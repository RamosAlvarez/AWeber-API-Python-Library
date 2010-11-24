from setuptools import setup, find_packages

setup(
    name='aweber_api',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    test_suite='nose.collector',
    url='http://labs.aweber.com/',
    include_package_data=True
)

