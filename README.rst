Introduction
============

.. contents::


`CGWB <http://cgwb-makinacorpus.rhcloud.com>`_ is a web interface to ``paster``, its goal is to generate a webinterface
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

You can even test it `here <http://cgwb-makinacorpus.rhcloud.com>`_

For now, we extensivly use templates from the `collective.generic.skel <https://github.com/collective/collective.generic.skel>`_ package


|cgwbthumb|_

.. |cgwbthumb| image:: https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb-min.png
.. _cgwbthumb: https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb.png

`Zoom <https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb.png>`_

Installation
==============

Installing cgwb
-----------------------------------

Install or update prerequisites
++++++++++++++++++++++++++++++++
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

If you want to work on the front end you must install nodejs.
Then use the make file to build the resources.

    make clean-resources
    make resources

Then you can watch the static_dev folder using 'grunt watch' command

    make watch

Generating & deploying your project
-----------------------------------------------------------
Launching the cgwb server
++++++++++++++++++++++++++++++++
Launch via ``bin/cgwb``.
This binary includes some options to let you override the default port (--port) and listenning address (--host)
To see all the available options, just use::

    ./l.sh

- At the moment, cgwb do not have some session mecanism, so the only way to replay a generation is to use the providen link in the generated tarball
- If you want to store your choices to redo an updated tarball later, just clink on the link providen by the file LINK_TO_REGENERATE.html in the produced tarball.

Filling the settings, some notes
+++++++++++++++++++++++++++++++++++++++++++
- project name is mandatory and must be in the form in `project` or `subproject`.


Credits
=======
Companies
---------
|makinacom|_

* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

People
------

- Mathieu Le Marec - Pasquet <kiorky@cryptelium.net>
- Jean-Philippe Camguilhem <jpc@makina-corpus.com>
- Jean-Michel FRANCOIS <toutpt@gmail.com>

.. _`minitage installation`: http://minitage.org/installation.html
.. _`cgwb`: http://localhost:6253
.. _`minitage`: http://www.minitage.org
