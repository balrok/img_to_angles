#!/usr/bin/env python

from distutils.core import setup
import pip
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=pip.download.PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='Image to Angle',
    version='1.0',
    description='Converts an image to a matrix of angles representing the outline',
    author='Carl Mai',
    author_email='carl.schoenbach@gmail.com',
    url='https://balrok.com',
    install_requires=reqs,
    py_modules=['img2angle', "b2i"],
   )
