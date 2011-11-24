Installation
==============

Installing cgwb in a minitage
-----------------------------------
You are not obliged to run with `minitage`_ even if it is the recommended mode for running at least the plones template.

Assuming that your minitage lives in ~/minitage, issue the following::

    export MT=~/minitage

Install or udpate minitage in your dedicated virtualenv if any
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Just do that (you must refer to `minitage installation`_ for prerequisites)

Install virtualenv
::

    virtualenv --no-site-packages --distribute $MT

Update minitage packages
::

    source $MT/bin/activate
    easy_install -U minitage.core
    easy_install -U minitage.paste
    minimerge -s


Install cgwb
++++++++++++++++++++++
Download & install via the minibuild
::

    source $MT/bin/activate
    git clone http://github.com/collective/collective.generic.webbuilder-minilay.git $MT/minilays/cgwb
    minimerge -v cgwb


Cgwb lives in ``$MT/bfg/cgwb``.

Generating & deploying your project using minitage
-----------------------------------------------------------
Launching the cgwb server
++++++++++++++++++++++++++++++++
Launch via ``bin/cgwb``.
This binary includes some options to let you override the default port (--port) and listenning address (--host)
To see all the available options, just use::

    bin/cgwb --help

If you use minitage, mandatory to use the minitage.instances.env profile::

    $MT/bin/easy_install -U minitage.paste
    $MT/bin/paster create -t minitage.instances.env cgwb

MINITAGE .ENV
++++++++++++++++++++
Each time you use cgwb, you use the .ENV::

    source $MT/bfg/cgwb/sys/share/minitage/minitage.env

Use it
++++++++++++++
Launch it::

    cd $INS
    ./bin/cgwb --port=6253


- At the moment, cgwb do not have some session mecanism, so the only way to replay a generation is to use the selenium firefox plugin.
- If you want to store your choices to redo an updated tarball later, just install the SeleniumIDE firefox plugin and use it to record your session.
- Maybe, activate selenium and

    - Go to the `cgwb`_
    - Choose `Generic Portal Plone3`.

Filling the settings, some notes
+++++++++++++++++++++++++++++++++++++++++++
- project name is mandatory and must be in the form in `project` or `subproject`.
- You can choose in the `Plone Products to auto checkout in development mode` the products from the community from which we should check out & use in development mode

THE IMPORTANT PART AROUND INITIATING A PROJECT
+++++++++++++++++++++++++++++++++++++++++++++++++
- It would be good unless you have some minitage experience to version the code prior to build, because of minitage update mecanism.
- Before version/import the code in your SCM you must elude the following points:

    * By default, the generated tarball contains the buildout layout and all the eggs in src, and the buildout use them as develop eggs and NOT WITH MR.DEVELOPER.
      Thus for running the buildout in standalone mode
    * You may decide not to include them as-is but to separate the code and version the code elsewhere.
    * I would advice you to checkout the packages with mr.developer.

An example of using svn which generic/pyramid
+++++++++++++++++++++++++++++++++++++++++++++
What i would do from a generated tarball for using subversion as my SCM could be to produce this layout::

    import
    |-- import/eggs
    |   |-- import/eggs/myproject.core
    |   |   `-- import/eggs/myproject.core/trunk
    `-- import/buildout


- Exporting base variables::

    export PROJECT="myproject" # your project name as filled in the web interfacE
    export TARBALL="$(ls -1t ~/cgwb/${PROJECT}-*.tar.gz|head -n1)" # produced tarball
    export IMPORT_URL="https://subversion.xxx.net/scrumpy/${PROJECT}/" # base svn place to import

- Create a temporary workspace::

    mkdir -p  $PROJECT/tarball
    cd $PROJECT
    tar xzvf  $TARBALL -C tarball/

- Create the base layout to be imported::

    mkdir -p import/buildout import/eggs

- Move the generated plone extensions eggs to a separate place to be imported::

    for i in tarball/src/${PROJECT}*;do if [[ -d $i ]] && [[ $(basename $i) != "themes" ]];then j=$(basename $i);dest=import/eggs/$j/trunk; mkdir -pv  $(dirname $dest); mv -v $i $dest; fi; done

- Move the buildout structure in the import layout::

    cp -rf tarball/* import/buildout

- Update buildout to use mr.developer instead of basic develop::

    * move off the develop declaration::

        sed -re "s:(src/)?$PROJECT\.((skin)|(tma)|(core)|(testing))::g" -i import//buildout/etc/project/$PROJECT.cfg

    * add to mr.developer sources::

        sed -re "/\[sources\]/{
        a $PROJECT.core = svn $IMPORT_URL/eggs/$PROJECT.core/trunk
        }" -i import/buildout/etc/project/sources.cfg

    * add to auto checkout packages::

        sed -re "/auto-checkout \+=/{
        a \    $PROJECT.core
        }"  -i import/buildout/etc/project/sources.cfg
        sed -re "/eggs \+=.*buildout:eggs/{
        a \    $PROJECT.core
        }"  -i import/buildout/etc/project/$PROJECT.cfg
        sed -re "/zcml \+=/{
        a \    $PROJECT.core
        }"  -i import/buildout/etc/project/$PROJECT.cfg

* be sure to use the right svn url to checkout::

    sed -re "s|src_uri.*|src_uri=$IMPORT_URL/buildout/|g" -i import/buildout/minilays/$PROJECT/*

* Be sure to use svn

    sed -re "s|src_type.*|src_type=svn|g" -i import/buildout/minilays/$PROJECT/*

* Import::

   svn import import/ $IMPORT_URL -m "initial import" 

An example of using svn which generic/plone
+++++++++++++++++++++++++++++++++++++++++++++
What i would do from a generated tarball for using subversion as my SCM could be to produce this layout::

    import
    |-- import/eggs
    |   |-- import/eggs/myproject.policy
    |   |   `-- import/eggs/myproject.policy/trunk
    |   |-- import/eggs/myproject.skin
    |   |   `-- import/eggs/myproject.skin/trunk
    |   |-- import/eggs/myproject.testing
    |   |   `-- import/eggs/myproject.testing/trunk
    |   `-- import/eggs/myproject.tma
    |       `-- import/eggs/myproject.tma/trunk
    `-- import/minitage
        |-- import/minitage/buildouts
        |   `-- import/minitage/buildouts/zope
        |       `-- import/minitage/buildouts/zope/myproject


- Exporting base variables::

    export PROJECT="myproject" # your project name as filled in the web interfacE
    export TARBALL="$(ls -1t ~/cgwb/${PROJECT}-*.tar.gz|head -n1)" # produced tarball
    export IMPORT_URL="https://subversion.xxx.net/scrumpy/${PROJECT}/ # base svn place to import

- Create a temporary workspace::

    mkdir -p  $PROJECT/tarball
    cd $PROJECT
    tar xzvf  $TARBALL -C tarball/

- Create the base layout to be imported::

    mkdir -p import/buildout import/eggs

- Move the generated plone extensions eggs to a separate place to be imported::

    for i in tarball/src/${PROJECT}*;do if [[ -d $i ]] && [[ $(basename $i) != "themes" ]];then j=$(basename $i);dest=import/eggs/$j/trunk; mkdir -pv  $(dirname $dest); mv -v $i $dest; fi; done

- Move the buildout structure in the import layout::

    cp -rf tarball/* import/buildout

- Update buildout to use mr.developer instead of basic develop::

    * move off the develop declaration::

        sed -re "s:(src/)?$PROJECT\.((skin)|(tma)|(policy)|(testing))::g" -i import//buildout/etc/project/$PROJECT.cfg

    * add to mr.developer sources::

        sed -re "/\[sources\]/{
        a $PROJECT.policy = svn $IMPORT_URL/eggs/$PROJECT.policy/trunk
        a $PROJECT.tma = svn $IMPORT_URL/eggs/$PROJECT.tma/trunk
        a $PROJECT.skin = svn $IMPORT_URL/eggs/$PROJECT.skin/trunk
        a $PROJECT.testing = svn $IMPORT_URL/eggs/$PROJECT.testing/trunk
        }" -i import/buildout/etc/project/sources.cfg

    * add to auto checkout packages::

        sed -re "/auto-checkout \+=/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        a \    $PROJECT.testing
        }"  -i import/buildout/etc/project/sources.cfg
        sed -re "/eggs \+=.*buildout:eggs/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        a \    $PROJECT.testing
        }"  -i import/buildout/etc/project/$PROJECT.cfg
        sed -re "/zcml \+=/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        }"  -i import/buildout/etc/project/$PROJECT.cfg

* be sure to use the right svn url to checkout::

    sed -re "s|src_uri.*|src_uri=$IMPORT_URL/buildout/|g" -i import/buildout/minilays/$PROJECT/*

* Be sure to use svn

    sed -re "s|src_type.*|src_type=svn|g" -i import/buildout/minilays/$PROJECT/*

* Import::

   svn import import/ $IMPORT_URL -m "initial import"

An example of using git which generic
++++++++++++++++++++++++++++++++++++++++
What i would do from a generated tarball for using subversion as my SCM could be to produce this layout::

    import
        |-- myproject.policy
        |-- myproject.skin
        |-- myproject.testing
        `-- myproject.tma
        `-- myproject.buildout
        `-- myproject.minilay


- Exporting base variables::

    export PROJECT="myproject"                                     # your project name as filled in the web interfacE
    export TARBALL="$(ls -1t ~/cgwb/${PROJECT}-*.tar.gz|head -n1)" # produced tarball
    export IMPORT_URL="ssh://git.makina-corpus.net/var/git"              # base svn place to import

- Create a temporary workspace & the base layout to be imported::

    mkdir -p  $PROJECT/
    cd $PROJECT
    mkdir tarball import
    tar xzvf  $TARBALL -C tarball/

- Move the generated plone extensions eggs to a separate place to be imported::

    for i in tarball/src/*;do if [[ -d $i ]] && [[ $i != "tarball/src/themes" ]];then j=$(basename $i);dest=import/$j;mkdir -pv  $(dirname $dest); mv -v $i $dest; fi; done

- Move the buildout structure in the import layout::

    cp -rf tarball/minilays/$PROJECT   import/$PROJECT.minilay
    rm -rf tarball/minilays
    cp -rf tarball/ import/$PROJECT.buildout

- Update buildout to use mr.developer instead of basic develop::

    * move off the develop declaration::

        sed -re "s:(src/)?$PROJECT\.((skin)|(tma)|(policy)|(testing))::g" -i import/$PROJECT.buildout/etc/project/$PROJECT.cfg

    * add to mr.developer sources::

        sed -re "/\[sources\]/{
        a $PROJECT.policy =  git $IMPORT_URL/$PROJECT.policy
        a $PROJECT.tma =     git $IMPORT_URL/$PROJECT.tma
        a $PROJECT.skin =    git $IMPORT_URL/$PROJECT.skin
        a $PROJECT.testing = git $IMPORT_URL/$PROJECT.testing
        }" -i import/$PROJECT.buildout/etc/project/sources.cfg

    * add to auto checkout packages::

        sed -re "/auto-checkout \+=/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        a \    $PROJECT.testing
        }"  -i import/$PROJECT.buildout/etc/project/sources.cfg
        sed -re "/eggs \+=.*buildout:eggs/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        a \    $PROJECT.testing
        }"  -i import/$PROJECT.buildout/etc/project/$PROJECT.cfg
        sed -re "/zcml \+=/{
        a \    $PROJECT.policy
        a \    $PROJECT.tma
        a \    $PROJECT.skin
        }"  -i import/$PROJECT.buildout/etc/project/$PROJECT.cfg

* be sure to use the right git url to checkout::

    sed -re "s|src_uri.*|src_uri=$IMPORT_URL/$PROJECT.buildout|g" -i import/*.minilay/*

* Be sure to use git

    sed -re "s|src_type.*|src_type=git|g" -i import/*.minilay/*

* Import::

   pushd import;for i in *;do echo "Importing $i";pushd $i;git init;git add *;git commit -am "initial revision";git remote add origin "$IMPORT_URL/$i";git push --all origin;popd;done;popd

Deploy the project
++++++++++++++++++++++
* install the minilay::

    export MT=~/minitage
    svn co $IMPORT_URL/buildout/minilays/$PROJECT/ $MT/minilays/$PROJECT
    # or
    git clone  $IMPORT_URL/$PROJECT.minilay $MT/minilays/$PROJECT

* Install it::

    minimerge -v $PROJECT

.. _`minitage installation`: http://minitage.org/installation.html
.. _`cgwb`: http://localhost:6253
.. _`minitage`: http://www.minitage.org

