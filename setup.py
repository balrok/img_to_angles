#!/usr/bin/env python3

from distutils.core import setup
import pip
import re
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

lib = "img2angles"
with open(lib + '/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(name=lib,
    version=version,
    description='Converts an image to a matrix of angles representing the outline',
    long_description=readme,
    author='Carl Mai',
    author_email='carl.schoenbach@gmail.com',
    url='https://balrok.com',
    install_requires=reqs,
    packages=[lib],
    classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'Environment :: Console', 
                'License :: OSI Approved :: MIT License',
                'Topic :: Multimedia :: Graphics',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
    ],
   )
