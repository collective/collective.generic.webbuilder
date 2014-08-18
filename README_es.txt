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

Por ahora, nosotros extensamente usamos plantillas de `collective.generic.skel <https://github.com/collective/collective.generic.skel>`_ package

Necesita una idea de lo que puede generar?, vea `Este ejemplo <https://github.com/makinacorpus/cgwb-test>`_

|cgwbthumb|_

.. |cgwbthumb| image:: https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb-min.png
.. _cgwbthumb: https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb.png

`Zoom <https://raw.github.com/collective/collective.generic.webbuilder/master/docs/cgwb.png>`_

Instalacion
==============

Instalando cgwb
-----------------------------------

Instale o actualice prerequisitos
++++++++++++++++++++++++++++++++++
::

    sudo apt-get install -y build-essential m4 libtool pkg-config autoconf gettext bzip2 groff man-db automake libsigc++-2.0-dev tcl8.5 git libssl-dev libxml2-dev libxslt1-dev libbz2-dev zlib1g-dev python-setuptools python-dev libjpeg62-dev libreadline-dev python-imaging wv poppler-utils libsqlite0-dev libgdbm-dev libdb-dev tcl8.5-dev tcl8.5-dev tcl8.4 tcl8.4-dev tk8.5-dev libsqlite3-dev

Instale cgwb
++++++++++++++++++++++
Descargue e instale via el minibuild
::

    git clone http://github.com/collective/collective.generic.webbuilder.git cgwb
    cd cgwb
    python bootstrap.py
    bin/buildout

Si usted necesita para trabajar en el frontend usted debera instalar nodejs.
Luego use el archivo make para construir los recursos.

    make clean-resources
    make resources

Luego usted puede ver la carpeta static_dev usando el comando 'grunt watch'

    make watch

Generando y desplegando su proyecto
-----------------------------------------------------------
Levantando el servidor cgwb
++++++++++++++++++++++++++++++++
Lancelo via ``bin/cgwb``.
Este binario incluye algunas opciones para dejarlo sobreescribir el puerto por defecto (--port) y la direccion de escucha (--host)
Para ver todas las opciones disponibles, solo use::

    ./l.sh

- Al momento, cgwb no tiene mecanismos de sesiones, asi que la unica forma de repetir la generacion es usar el link provisto en el tarball generado
- Si usted necesita guardar sus selecciones y rehacer un tarball actualizado luego, solo clickee en el link suministrado por el archivo LINK_TO_REGENERATE.html en el tarball producido.

Llenando las configuraciones, algunas notas
++++++++++++++++++++++++++++++++++++++++++++++
- El nombre del proyecto es obligatorio y debe estar en el formulario como `project` o `subproject`.


Creditos
=========
Compañias
---------
|makinacom|_

* `Contacto Makina Corpus <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

Personas
---------

- Mathieu Le Marec - Pasquet <kiorky@cryptelium.net>
- Jean-Philippe Camguilhem <jpc@makina-corpus.com>
- Jean-Michel FRANCOIS <toutpt@gmail.com>

.. _`minitage installation`: http://minitage.org/installation.html
.. _`cgwb`: http://localhost:6253
.. _`minitage`: http://www.minitage.org
