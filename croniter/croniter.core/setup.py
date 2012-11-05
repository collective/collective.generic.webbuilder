import os, sys

from setuptools import setup, find_packages

version = "1.0dev"

def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.txt'),
     read('docs', 'INSTALL.txt'),
     read('docs', 'HISTORY.txt'),
    ]
)

classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development",]



name = 'croniter.core'
setup(
    name=name,
    namespace_packages=[         'croniter',
    ],              
    version=version,
    description='Project libertic.event',
    long_description=long_description,
    classifiers=classifiers,
    keywords='',
    author='kiorky',
    author_email='kiorky@localhost',
    url='http://pypi.python.org/pypi/%s' % name,
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    extras_require = {
        'test': ['ipython', 'plone.testing']
    },
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    # define there your console scripts
    entry_points = {
        'console_scripts': [
            'core = croniter.core.core:main',
        ],
    }

)
# vim:set ft=python:
