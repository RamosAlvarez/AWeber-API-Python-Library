from setuptools import setup, find_packages

setup(
    name='aweber_api',
    version='1.0.1',
    packages=find_packages(exclude=['tests']),
    url='http://labs.aweber.com/',
    install_requires = ['oauth2 >= 1.2'],
    include_package_data=True
)

