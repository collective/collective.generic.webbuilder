Introduction
============

.. contents::


CGWB is a web interface to ``paster``, its goal is to generate a webinterface
to selection options aggregated from a set of templates.

Imagine that you have 2 templates, the one that can deploy an application,
and the other which generates the application in itself.

Declaring the two templates as a ``cgwb set`` will make a webinterface for
those 2 templates. Answering correctly to the questions will produce a tarball
that you ll be able download and unpack to have your base installation setup.

To make the templates available, you must define the set using ZCML.

As this server was developped as a quick and efficient interface to paster,
*it is not safe to open it to wide internet.*
For security reason, just launch/use when you need it.

Next versions will include some sessions/roles and improved security,
it may be possible at this stage to leave it open.

For now, we extensivly use templates from the `collective.generic.skel <https://github.com/collective/collective.generic.skel>`_ package


|cgwbthumb|_

.. |cgwbthumb| image:: https://raw.github.com/collective/collective.generic.webbuilder/master/cgwb-min.jpeg
.. _cgwbthumb: https://raw.github.com/collective/collective.generic.webbuilder/master/cgwb.jpeg

`Zoom <http://distfiles.minitage.org/public/externals/minitage/cgwb.jpeg>`_

Installation
==============

Installing cgwb
-----------------------------------

Install or udpate minitage in your dedicated virtualenv if any
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
::

    sudo apt-get install -y build-essential m4 libtool pkg-config autoconf gettext bzip2 groff man-db automake libsigc++-2.0-dev tcl8.5 git libssl-dev libxml2-dev libxslt1-dev libbz2-dev zlib1g-dev python-setuptools python-dev libjpeg62-dev libreadline-dev python-imaging wv poppler-utils libsqlite0-dev libgdbm-dev libdb-dev tcl8.5-dev tcl8.5-dev tcl8.4 tcl8.4-dev tk8.5-dev libsqlite3-dev

Install cgwb
++++++++++++++++++++++
Download & install via the minibuild
::

    git clone http://github.com/collective/collective.generic.webbuilder.git cgwb
    cd cgwb
    python bootstrap.py
    bin/buildout

Generating & deploying your project using minitage
-----------------------------------------------------------
Launching the cgwb server
++++++++++++++++++++++++++++++++
Launch via ``bin/cgwb``.
This binary includes some options to let you override the default port (--port) and listenning address (--host)
To see all the available options, just use::

    ./l.sh

- At the moment, cgwb do not have some session mecanism, so the only way to replay a generation is to use the providen link in the generated tarball
- If you want to store your choices to redo an updated tarball later, just clink on the link.

Filling the settings, some notes
+++++++++++++++++++++++++++++++++++++++++++
- project name is mandatory and must be in the form in `project` or `subproject`.


Credits
=======
Companies
---------
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

Authors
-------

- kiorky <kiorky@cryptelium.net>
- Jean-Philippe Camguilhem <jpc@makina-corpus.com>

.. _`minitage installation`: http://minitage.org/installation.html
.. _`cgwb`: http://localhost:6253
.. _`minitage`: http://www.minitage.org
