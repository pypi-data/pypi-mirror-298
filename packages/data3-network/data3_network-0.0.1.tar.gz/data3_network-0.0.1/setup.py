from setuptools import setup, find_packages

setup(
    name='data3_network',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'syft==0.9.1',
    ],
    author='Data3 Network',
    author_email='data3network@gmail.com',
    description='Data3 Network Library for PySyft Server Integration',
)


