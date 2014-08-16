Introduccion
============

.. contenido::


`CGWB <http://cgwb-makinacorpus.rhcloud.com>`_ es una interfaz web para ``paster``, su meta es generar una interfaz web para seleccionar opciones agregadas en base a unas plantillas.

Imagine que usted tiene 2 plantillas, la primera que usted puede hacer deploy de una aplicacion,
y la otra que genera la aplicacion por si sola.

Declarando las dos plantillas como ``cgwb set`` les dara una interfaz web para esas dos plantillas.
Respondiendo correctamente las preguntas, este generara un tarball que estara disponible para descargar y descomprimir, y asi tener el setup basico para la instalacion.

Para tener las plantillas disponibles, usted debera definir el uso de ZCML.

Como este servidor ha sido desarrollado como una rapida y eficiente interfaz para paster,
*No es seguro abrirlo a todo el ancho del internet.*
Por razones de seguridad, solo lance/use cuando lo necesite.

Usted puede probarlo `aqui <http://cgwb-makinacorpus.rhcloud.com>`_

For now, we extensivly use templates from the `collective.generic.skel <https://github.com/collective/collective.generic.skel>`_ package


Want an idea of what it can generate, see `This example <https://github.com/makinacorpus/cgwb-test>`_

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
