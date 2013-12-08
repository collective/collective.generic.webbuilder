from setuptools import setup, find_packages
import os

version = '1.2dev'


def read(rnames):
    setupdir = os.path.dirname(os.path.abspath(__file__))
    return open(
        os.path.join(setupdir, *rnames)
    ).read()

README = read((os.path.dirname(__file__), 'README.rst'))
INSTALL = read((os.path.dirname(__file__), 'docs', 'INSTALL.rst'))
CHANGELOG = read((os.path.dirname(__file__), 'docs', 'CHANGES.txt'))
TESTS_DIR = (
    os.path.dirname(__file__), 'src',
    'collective', 'generic', 'webbuilder', 'tests'
)
tdt = """
Tests & docs
==============
"""
TESTS = '%s' % (
    '\n' + tdt +
    read(TESTS_DIR + ('test_zcml.txt',)) + '\n' +
    read(TESTS_DIR + ('test_paster.txt',)) + '\n' +
    read(TESTS_DIR + ('test_plugins.txt',)) + '\n' +
    read(TESTS_DIR + ('browser.txt',)) + '\n' +
    '\n'
)
long_description = '\n'.join([README,
                              INSTALL,
                              TESTS,
                              CHANGELOG]) + '\n'

APP_requires = [
    'collective.generic.skel',
    'collective.generic.devmode',
    'WebOb',
    'zope.component',
    'pyramid',
    'pyramid_zcml',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'iniparse',
    'repoze.vhm',
    'waitress',
    'PasteDeploy',
    'Paste',
    'Pastescript',
]

setup(
    name='collective.generic.webbuilder',
    version=version,
    description="Yet another WSGI Paste factory for paste by Makina Corpus",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Mathieu Pasquet, Jean-Philippe Camguilhem',
    author_email=(
        'kiorky@cryptelium.net, '
        'jean-philippe.camguilhem@makina-corpus.com'),
    url='http://pypi.python.org/pypi/collective.generic.webbuilder',
    license='BSD',
    namespace_packages=['collective',
                        'collective.generic',
                        ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'app': APP_requires,
        'test': ['ipython',
                 'zope.testing',
                 'lxml',
                 'zope.testbrowser']},
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    # do not add directly deps here to have a mean with
    # sed to remove them on openshift before deploy hook
    install_requires=['setuptools'] + APP_requires,
    entry_points={
        'paste.app_factory': ['cgwb=collective.generic.webbuilder:main'],
        'paste.paster_create_template': [
        ],
    },
)
