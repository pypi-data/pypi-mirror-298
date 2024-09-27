# setup.py
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='RDGen',
    version='1.0.1',
    description='A reusable 2D dungeon generator for Python projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Robert Tilton',
    author_email='RobertJTilton89@gmail.com',
    packages=find_packages(),
    install_requires=[
        "colorama==0.4.6",
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
