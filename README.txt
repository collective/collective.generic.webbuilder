==========================
Introduction
==========================

.. contents::


CGWB is a web interface to ``paster``, its goal is to generate a webinterface to selection options aggregated from a set of templates.

Imagine that you have 2 templates, the one that can deploy an application, and the other which generates the application in itself.

Declaring the two templates as a ``cgwb set`` will make a webinterface for those 2 templates. Answering correctly to the questions will produce a tarball that you ll be able download and unpack to have your base installation setup.

To make the templates available, you must define the set using ZCML.


As this server was developped as a quick and efficient interface to paster, *it is not safe to open it to wide internet.*
For security reason, just launch/use when you need it.

Next versions will include some sessions/roles and improved security, it may be possible at this stage to leave it open.


Makina Corpus sponsorised software
======================================
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
