from setuptools import setup
from setuptools import find_packages


def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='mysudoku',
    version='1.3',
    author='Murtada Altarouti',
    author_email='murtada.altarouti@gmail.com',
    description='A Sudoku generator and solver',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
)
