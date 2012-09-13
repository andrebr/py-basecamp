#!/usr/bin/env python
from setuptools import setup, find_packages
from basecamp.version import get_version

setup(
    name='basecamp',
    version=get_version(),
    description=('A python interface to the Basecamp Next API '
        'using python-requests'),
    long_description=open('README.rst').read(),
    author='Greg Aker',
    author_email='greg@ngenworks.com',
    license='BSD',
    keywords='basecamp api',
    url='https://github.com/ngenworks/py-basecamp.git',
    packages=find_packages(),
    test_suite='nose.collector',
    tests_require=['nose', ],
    install_requires=['requests>=0.14.0', ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
