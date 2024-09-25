# coding=utf-8

from distutils.core import setup

from setuptools import find_packages


def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    reqs = []
    for line in lines:
        line = line.strip()
        if not line.startswith('--') and line:
            reqs.append(line)
    return reqs


setup(
    name='octopus-common-python',
    version='1.0.6b39',
    author='xzhao32',
    author_email='xzhao32@trip.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        'console_scripts': [
            'octopus=octopus_common.util.crawler_command_utils:main'
        ],
    },
)
