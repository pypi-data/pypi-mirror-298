from setuptools import setup, find_packages

with open("LICENSE.txt", "r") as f:
    description = f.read()

setup(
    name='Open_Excel_Processor',
    version='0.3.3',
    description='A library to interact with Excel files and process data',
    author='Cobra Author',
    author_email='cobraauthor@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'datetime'
    ],
    long_description=description
)
