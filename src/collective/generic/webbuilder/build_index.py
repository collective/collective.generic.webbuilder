from paste.script.templates import Template
from generic.policy.package import Package

def checked(var):
    if var.default == True:
        return 'checked="checked"'
    else:
        return ''

def build_index():

    index = Package(Template)

    text = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="alternate" type="application/rss+xml" title="Feed Title" href="_static/feed.xml" />
        <link rel="alternate" type="application/rss+xml" title="Feed Title" href="_static/devs_feed.xml" />

        <title>Welcome to Makina-Corpus Plone generator</title>
        <link rel="stylesheet" href="_static/makina.css" type="text/css" />
        <link rel="shortcut icon" href="_static/favicon.ico"/>
      </head>
      <body>
          <div class="document">
            <div id="header">
                <h1>Makina-Corpus</h1>
                <h2>Plone Portal Generator</h2>
            </div>
            <form action="paster.py">

       """
    plone = [var for var in Package.vars if var.name=='plone'][0].default
    prod_port = [var for var in Package.vars if var.name=='prod_port'][0].default
    prod_path = [var for var in Package.vars if var.name=='prod_path'][0].default
    val_vers = [var for var in Package.vars if var.name=='utils_valid_versions'][0]

    text += '<p><input type="checkbox" name="%s" %s>%s</p> ' % (val_vers.name,
                                                                checked(val_vers),
                                                                val_vers.description)
    text += """
            <div class="related">
           <fieldset style="float: left;">
                <legend>Projet</legend>
           <div><label>namespace_package</label><input name="namespace_package" value="myproject"/></div>
           """



    text += '<div><label>Plone version ( >=3.2.1 )</label><input name="plone" value="%s"/></div>' % plone
    text += '</fieldset>'
    text += '<fieldset style="float: right;"> <legend>Production</legend> '
    text += '<div><label>Production port</label><input name="prod_port" value="%s"/></div>' % prod_port
    text += '<div><label>Production path</label><input name="prod_path" value="%s"/></div>' % prod_path
    text += '</fieldset>'

    products = [var for var in Package.vars if var.default in [True, False] and not var.name.startswith('utils')]
    middle = len(products) / 2 + len(products) % 2

    #left block
    text += '<fieldset style="float: left;">'
    for product in products[:middle]:
        text += '<div><input type="checkbox" name="%s" %s>%s</div> ' % (product.name,
                                                                                checked(product),
                                                                                product.description)
    text += '</fieldset><fieldset style="float: right;">'
    #right block
    for product in products[middle:]:
        text += '<div><input type="checkbox" name="%s" %s>%s</div> ' % (product.name,
                                                                                 checked(product),
                                                                                 product.description)
    text += '</fieldset>'

    end_text ="""

    <input type=submit value="create">
    </div>
    </form>
    </body>
    </html>
    """
    try:
        f = open('index.html', 'w')
        f.write(text+end_text)
    finally:
        f.close()
