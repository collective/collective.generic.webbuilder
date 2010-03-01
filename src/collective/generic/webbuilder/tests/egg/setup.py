from setuptools import setup, find_packages
import os

version = '1.0'

def read(rnames):
    setupdir =  os.path.dirname( os.path.abspath(__file__))
    return open(
        os.path.join(setupdir, *rnames)
    ).read()


long_description =''
setup(
    name='cgwb.tp',
    version=version,
    description="Yet another WSGI Paste factory for paste",
    long_description=long_description,
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Mathieu Pasquet',
    author_email='mpakiorky@cryptelium.net',
    url='',
    license='BSD',
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    extras_require={'test': ['ipython', 'zope.testing', 'lxml']},
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[ 'setuptools', ],
    entry_points={
        'paste.paster_create_template': [
            'cgwb.testpackage1 = tp.package:Package',
            'cgwb.testpackage2 = tp1.package:Package',
            'cgwb.testpackage3 = tp2.package:Package',
        ],
    },
)

