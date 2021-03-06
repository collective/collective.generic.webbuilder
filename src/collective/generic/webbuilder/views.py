import os
import traceback
import re
import pkg_resources
from uuid import uuid4
import tarfile
import urllib
import shutil
import urllib2
import zlib
import datetime

from zope import component
from Cheetah import Parser

from pyramid.renderers import render_to_response
from pyramid import renderers
get_template = renderers.get_renderer
from pyramid.static import static_view


from pyramid.threadlocal import get_current_registry

from collective.generic.webbuilder.interfaces import *
from collective.generic.webbuilder.models import root
from collective.generic.webbuilder.paster import (
    PasterAssembly,
    NoSuchConfigurationError,
)

from webob import Response

from collective.generic.webbuilder.utils import remove_path

sm = component.getSiteManager()
gsm = component.getGlobalSiteManager()


def download_static_view(context, request):
    request.subpath = tuple(context.path.split('/'))
    return static_view(get_generation_path(), use_subpath=True)


def webbuilder_view(context, request):
    main = get_template('templates/main_template.pt').implementation()

    return render_to_response(
        'templates/index.pt',
        {'root': root,
         'main': main,
         'errors': {}},
        request=request,)


def get_generation_path():
    s = get_current_registry().settings
    dp = s['gen_path']
    if not os.path.exists(dp):
        os.makedirs(dp)
    return dp


def postprocess(paster, output_dir_prefix, project_name, params):

    plugin_names = paster.configuration.plugins[:]
    plugin_names.sort(lambda a, b: a[1] - b[1])
    plugin_names = [p[0] for p in plugin_names]
    for plugin_name in plugin_names:
        plugin = gsm.queryAdapter(paster,
                                  IPostGenerationPlugin,
                                  name=plugin_name)
        if plugin:
            plugin.process(output_dir_prefix, project_name, params)


def get_paster(configuration):
    pastero = PasterAssembly(configuration)
    paster = IPasterAssemblyReader(pastero)
    paster.read()
    return paster.paster


def webbuilder_process(context, request):
    valid_actions = ['submit_cgwbDownload']
    errors = []
    output_dir_prefix = None
    params = dict(request.params)
    actions = [action for action in request.params
               if re.match('^submit_', action)]
    [params.pop(action) for action in actions]
    configuration = params.pop('configuration', None)
    download_path = None
    if not configuration:
        errors.append('Choose a configuration')
    if not configuration in root.configurations:
        errors.append('Invalid configurations')
    if not errors:
        for action in actions:
            output_dir_prefix = os.path.join(
                get_generation_path(), "%s" % uuid4())
            if action in valid_actions:
                try:
                    paster = get_paster(configuration)
                    createcmd = [
                        a
                        for a in pkg_resources.iter_entry_points(
                            'paste.global_paster_command',
                            'create')
                    ][0].load()
                    [params.update({param: True})
                     for param in params
                     if params[param] in [u'on', u'checkbox_enabled']]
                    project = params.pop('project', None)
                    if not project:
                        project = ''
                    project = project.strip()
                    if not project:
                        raise Exception('Project does not exist or is empty')
                    if (
                        os.path.exists(output_dir_prefix)
                        and len(os.listdir(output_dir_prefix)) > 0
                    ):
                        if (
                            not get_settings().get(
                                'debug', '').lower() == 'true'
                        ):
                            raise Exception('Directory %s exists '
                                            'and is not empty' % (
                                                output_dir_prefix))
                    # keep track of boolean options for descendant templates
                    boolean_consumed_options = {}
                    for template in paster.templates_data:
                        cparams = params.copy()
                        output_dir = output_dir_prefix
                        if template['self'].output:
                            output_dir = os.path.join(output_dir,
                                                      template['self'].output)
                        top = [
                            '-q',
                            '-t', template['name'],
                            '--no-interactive',
                            '-o', output_dir,
                            project
                        ]
                        if template['aliases']:
                            for var, alias, default in template['aliases']:
                                # we have a value
                                if alias in cparams:
                                    cparams[var.name] = cparams[alias]
                                #blank value, resetting
                                else:
                                    if var.name in cparams:
                                        del cparams[var.name]

                        # set to false unticked options
                        for g in template['groups']:
                            for myo in g['options']:
                                if myo[1] == 'boolean':
                                    boolean_consumed_options[myo[0].name] = (
                                        cparams.get(myo[0].name, False))
                        for option in boolean_consumed_options:
                            if not option in cparams:
                                    cparams[option] = False

                        # cleanup variables
                        names = dict([(var.name, var)
                                      for var in template['template'].vars])
                        for iv in cparams.keys():
                            if not iv in names:
                                del cparams[iv]
                                continue
                            else:
                                if not cparams[iv]:
                                    if not names[iv].default:
                                        del cparams[iv]
                                        continue

                        # be sure not to have unicode params there
                        # because paster will swallow them up
                        top.extend(
                            ["%s=%s" % i for i in cparams.items()]
                        )
                        cmd = createcmd('create')
                        try:
                            cmd.run(top)
                        except Exception, e:
                            remove_path(output_dir)
                            raise
                    # do post genration stuff
                    postprocess(paster, output_dir_prefix, project, params)

                    if action == 'submit_cgwbDownload':
                        qsparams = dict(request.POST)
                        qsparams.update(params)
                        qsparams.update(boolean_consumed_options)
                        qs = urllib.urlencode(qsparams)
                        ficp = os.path.join(output_dir_prefix,
                                            'LINK_TO_REGENERATE.html')
                        burl = request.route_url(
                            'collect',
                            configuration=request.POST.get('configuration'))
                        genurl = burl + '?%s' % urllib.urlencode(
                            dict(oldparams=zlib.compress(
                                qs, 9).encode('base64')))
                        fic = open(ficp, 'w')
                        fic.write(
                            '<html><body>'
                            '<a href="%s">'
                            'Click here to go to the generation service</a>'
                            '</body></html>' % genurl)
                        fic.close()
                        ts = '%s' % datetime.datetime.now()
                        ts = ts.replace(':', '-').replace(' ', '_')[:-4]
                        filename = '%s-%s.tar.gz' % (project, ts)
                        file_path = os.path.join(get_generation_path(),
                                                 filename)
                        fic = tarfile.open(file_path, 'w:gz')
                        fic.add(output_dir_prefix, './')
                        fic.close()
                        download_path = os.path.basename(file_path)
                        resp = Response(
                            body=open(file_path).read(),
                            content_type='application/x-tar-gz',
                            headerlist=[
                                ('Content-Disposition',
                                 str('attachment; filename="%s"' % (
                                     os.path.basename(file_path)))),
                                ('Content-Transfer-Encoding', 'binary'),
                                ('Content-Length', '%s' % (
                                    os.path.getsize(file_path))),
                            ],
                            request=request,
                        )
                        os.remove(file_path)

                        return resp
                except NoSuchConfigurationError:
                    errors.append(
                        '%s/ The required configuration '
                        'does not exists : %s' % (
                            action, configuration)
                    )
                except Parser.ParseError, e:
                    errors.append(
                        '<div class="error">'
                        '<p>%s/ Error while reading paster variables:</p>'
                        '<p class="pythonerror">%r</p>'
                        '<p class="pythonerror"><pre>%s</pre></p>'
                        '</div>' % (action, e, e.report())
                    )
                except Exception, e:
                    trace = traceback.format_exc()
                    # raise
                    errors.append(
                        '<div class="error">'
                        '<p>%s/ -- Error while reading paster variables:</p>'
                        '<p class="pythonerror">%r</p>'
                        '<p class="pythonerror">%s</p>'
                        '<p class="pythonerror"><pre>%s</pre>/p>'
                        '</div>' % (action, e, e, trace)
                    )
                finally:
                    remove_path(output_dir_prefix)
    main = get_template('templates/main_template.pt').implementation()

    return render_to_response(
        'templates/process.pt',
        dict(errors=errors,
             context=context,
             root=root,
             output=output_dir_prefix,
             download_path=download_path,
             main=main),
        request=request,
    )


def webbuilder_collectinformation(context, request):
    errors, added_options = [], []
    paster, default_group_data, templates_data = None, None, None
    try:
        if 'oldparams' in request.GET:
            original_qs = zlib.decompress(
                request.GET.get('oldparams').decode('base64'))
            #redir = request.route_url(
            #    'collect',
            #    configuration=context.configuration) + '?%s' % original_qs
            pms = urllib2.urlparse.parse_qs(original_qs)
            params = dict([(a, pms[a][0]) for a in pms])
            request.GET.update(params)
        paster = get_paster(context.configuration)
        templates_data = paster.templates_data
    except NoSuchConfigurationError:
        errors.append(
            'The required configuration '
            'does not exists : %s' % context.configuration)
    except Exception, e:
        raise
        errors.append(
            'Error while reading paster variables: <pre>%r</pre>' % e)
    main = get_template('templates/main_template.pt').implementation()

    return render_to_response(
        'templates/collect.pt',
        dict(errors=errors,
             context=context,
             main=main,
             root=root,
             templates=templates_data,
             pair_options=pair_options,
             get_value=get_value),
        request=request,
    )


def get_value(template, aliasname, default=None):
    res = default
    if aliasname:
        for var, alias, default in template['aliases']:
            # we have a value
            if aliasname == alias:
                res = default
    return res


def pair_options(l):
    if not l:
        return l
    values = []
    for ix, i in enumerate(l):
        if ix % 2 == 0:
            cur = []
            values.append(cur)
        cur.append(i)
    return values
