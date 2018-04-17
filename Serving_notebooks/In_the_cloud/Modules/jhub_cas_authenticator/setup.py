#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import sys

from setuptools import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name                = 'uva-jhub_cas_authenticator',
    packages            = ['jhub_cas_authenticator'],
    version             = '1.0',
    description         = """CAS Authenticator: An Authenticator for Jupyterhub that authenticates against an external CAS service.""",
    long_description    = "",
    author              = "Carl (https://github.com/cwaldbieser)",
    author_email        = "",
    url                 = "https://github.com/cwaldbieser/jhub_cas_authenticator",
    license             = "GPLv3",
    platforms           = "Linux, Mac OS X",
    keywords            = ['Interactive', 'Interpreter', 'Shell', 'Web'],
    classifiers         = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    install_requires.append('jupyterhub')

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
