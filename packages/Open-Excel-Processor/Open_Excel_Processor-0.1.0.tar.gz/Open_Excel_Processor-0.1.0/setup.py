from setuptools import setup, find_packages

with open("LICENSE.txt", "r") as f:
    description = f.read()

setup(
    name='Open_Excel_Processor',
    version='0.1.0',
    description='A library to interact with Excel files and process data',
    author='Cobra Author',
    author_email='cobraauthor@gmail.com',
    packages=find_packages(),
    install_requires=[
        'openpyxl',
        'requests',
        'firebase-admin'
    ],
    long_description=description
)
