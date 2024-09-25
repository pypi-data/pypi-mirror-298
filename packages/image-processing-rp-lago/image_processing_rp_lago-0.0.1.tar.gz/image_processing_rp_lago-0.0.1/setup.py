from setuptools import setup, find_packages
import os

with open('README.md', 'r') as f:
    page_description = f.read()

requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')

with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='image-processing-rp-lago',
    version='0.0.1',
    author='Robson P Lago',
    author_email='robson.pereira.lago@gmail.com',
    description='A package for image processing',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RP-Lago/IMAGE_PROCESSING_PACKAGE.git',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12.6',
)