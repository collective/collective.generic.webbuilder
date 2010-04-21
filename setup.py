from setuptools import setup, find_packages
import os

version = '1.0'

def read(rnames):
    setupdir =  os.path.dirname( os.path.abspath(__file__))
    return open(
        os.path.join(setupdir, *rnames)
    ).read()

README =read((os.path.dirname(__file__),'README.txt'))
CHANGELOG  = read((os.path.dirname(__file__), 'docs', 'HISTORY.txt'))
TESTS_DIR = os.path.dirname(__file__), 'src', 'collective', 'generic','webbuilder', 'tests'
tdt = """
Tests & docs
==============
"""
TESTS  = '%s' % (
    '\n'+tdt+
    read(TESTS_DIR + ('test_zcml.txt',)) + '\n' +
    read(TESTS_DIR + ('test_paster.txt',)) + '\n' +
    read(TESTS_DIR + ('test_plugins.txt',)) + '\n' +
    read(TESTS_DIR + ('browser.txt',)) + '\n' +
    '\n'
)
long_description = '\n'.join([README,
                              TESTS,
                              CHANGELOG])+'\n'
setup(
    name='collective.generic.webbuilder',
    version=version,
    description="Yet another WSGI Paste factory for paste sponsorised by Makina Corpus",
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Mathieu Pasquet, Jean-Philippe Camguilhem',
    author_email='kiorky@cryptelium.net, jean-philippe.camguilhem@makina-corpus.com',
    url='https://subversion.makina-corpus.net/zopina/eggs/collective.generic.webbuilder/trunk',
    license='BSD',
    namespace_packages=['collective', 'collective.generic', 'collective.generic.webbuilder'],
    include_package_data=True,
    zip_safe=False,
    extras_require={'test': ['ipython', 'zope.testing', 'lxml', 'zope.testbrowser', 'repoze.vhm']},
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[
        'setuptools',
        'collective.generic.skel',
        'minitage.paste',
        'WebOb',
        'z3c.form',
        'repoze.bfg',
    ],
    entry_points={
        'paste.app_factory': ['cgwb_app=collective.generic.webbuilder.webserver:wsgi_app_factory',],
        'console_scripts': ['cgwb=collective.generic.webbuilder.webserver:main',],
        'paste.paster_create_template': [
            #'cgwb.testpackage1 = collective.generic.webbuilder.tests.tp.package:Package',
            #'cgwb.testpackage2 = collective.generic.webbuilder.tests.tp1.package:Package',
            #'cgwb.testpackage3 = collective.generic.webbuilder.tests.tp2.package:Package',
        ],
    },
)

