import os
import re
import pkg_resources
import tempfile
import tarfile
import datetime

from zope import component
from Cheetah import Parser



from repoze.bfg.chameleon_zpt import render_template_to_response
from repoze.bfg.chameleon_zpt import get_template
from repoze.bfg.view import static
from repoze.bfg.settings import get_settings

from collective.generic.webbuilder.interfaces import *
from collective.generic.webbuilder.models import root
from collective.generic.webbuilder.paster import (
    PasterAssembly,
    NoSuchConfigurationError,
)

try:
    from minitage.core.common import remove_path, MinibuildNotFoundException
except:
    print "Upgrade minitage.core please! (maybe delete it to get it reinstalled in your buildout egg cache if any)"
from webob import Response

sm = component.getSiteManager()
gsm = component.getGlobalSiteManager()

def download_static_view(context, request):
    request.subpath = tuple(context.path.split('/'))
    return static(get_generation_path())(context, request)

def webbuilder_view(context, request):
    main = get_template('templates/main_template.pt')

    return render_template_to_response(
        'templates/index.pt',
        request = request,
        root=root,
        main=main,
        errors=[],)

def get_generation_path():
    s = get_settings()
    dp = os.getcwd()
    if s:
        dp = s.get('generation_path', dp)
    return dp

def postprocess(paster, output_dir_prefix, project_name, params):

    plugin_names = paster.configuration.plugins[:]
    plugin_names.sort(lambda a,b: a[1] - b[1])
    plugin_names = [p[0] for p in plugin_names]
    for plugin_name in plugin_names:
        plugin = gsm.queryAdapter(paster, IPostGenerationPlugin, name = plugin_name)
        if plugin:
            plugin.process(output_dir_prefix, project_name, params)

def get_paster(configuration):
    pastero = PasterAssembly(configuration)
    paster = IPasterAssemblyReader(pastero)
    paster.read()
    return paster.paster

def webbuilder_process(context, request):
    valid_actions = ['submit_cgwbDownload', 'submit_cgwbGenerate']
    errors = []
    output_dir_prefix = None
    params = dict(request.params)
    actions = [action for action in request.params if re.match('^submit_', action)]
    noecho = [params.pop(action) for action in actions]
    configuration = params.pop('configuration', None)
    download_path = None
    if not configuration:
        errors.append('Choose a configuration')
    if not configuration in root.configurations:
        errors.append('Invalid configurations')
    if not errors:
        for action in actions:
            if action in valid_actions:
                try:
                    paster = get_paster(configuration)
                    createcmd = [a
                     for a in pkg_resources.iter_entry_points(
                         'paste.global_paster_command',
                         'create')
                                ][0].load()
                    noecho = [params.update({param: True})
                              for param in params if params[param] in [u'on', u'checkbox_enabled']]
                    project = params.pop('project', None)
                    if not project:
                        project = ''
                    project = project.strip()
                    if not project:
                        raise Exception('Project does not exist or is empty')
                    if action == 'submit_cgwbDownload':
                        output_dir_prefix = tempfile.mkdtemp()
                    else:
                        output_dir_prefix = os.path.join(get_generation_path(), project)
                    if os.path.exists(output_dir_prefix) and len(os.listdir(output_dir_prefix))>0:
                        if not get_settings().get('debug', '').lower() == 'true' :
                            raise Exception('Directory %s exists and is not empty' % output_dir_prefix)
                    # keep track of boolean options for descendant templates
                    boolean_consumed_options = []
                    for template in paster.templates_data:
                        cparams = params.copy()
                        output_dir = output_dir_prefix
                        if template['self'].output:
                            output_dir = os.path.join(output_dir, template['self'].output)
                        top = ['-q',
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
                                    boolean_consumed_options.append(myo[0].name)
                        for option in boolean_consumed_options:
                            if not option in cparams:
                                    cparams[option] = False

                        # cleanup variables
                        names = dict([(var.name,var) for var in template['template'].vars])
                        for iv in cparams.keys():
                            if not iv in names:
                                del cparams[iv]
                                continue
                            else:
                                if not cparams[iv]:
                                    if not names[iv].default:
                                        del cparams[iv]
                                        continue


                        # be sure not to have unicode params there because paster will swallow them up
                        top.extend(
                            ["%s=%s" % i for i in cparams.items()]
                        )
                        cmd = createcmd('create')
                        try:
                            ret = cmd.run(top)
                        except Exception, e:
                            remove_path(output_dir)
                            raise
                    # do post genration stuff
                    postprocess(paster, output_dir_prefix, project, params)

                    if action == 'submit_cgwbDownload':
                        ts = '%s'%datetime.datetime.now()
                        ts = ts.replace(':', '-').replace(' ', '_')[:-4]
                        filename = '%s-%s.tar.gz' % (project, ts)
                        file_path = os.path.join(get_generation_path(), filename)
                        fic = tarfile.open(file_path, 'w:gz')
                        fic.add(output_dir_prefix, './')
                        fic.close()
                        download_path = os.path.basename(file_path)
                        resp = Response(
                            body = open(file_path).read(),
                            content_type = 'application/x-tar-gz',
                            headerlist = [
                                ('Content-Disposition',
                                 'attachment; filename="%s"' % os.path.basename(file_path)
                                ),
                                ('Content-Transfer-Encoding', 'binary')
                            ],
                            request = request,
                        )
                        os.remove(file_path)
                        return resp
                except NoSuchConfigurationError:
                    errors.append(
                        '%s/ The required configuration '
                        'does not exists : %s' % (
                            action, configuration)
                    )
                except MinibuildNotFoundException, e:
                    #raise
                    errors.append(
                        '<div class="error">'
                        '<p>%s/ Error while reading paster variables:</p>'
                        '<p class="pythonerror">%r</p>' 
                        '<br/><p>Are you inside a minitage ? </p>'
                        '<br/><ul><li> If no, please untick minitage support in the minitage '
                        'section (press your browser\'s back button)</p>'
                        '<br/><li> If yes, you must set the "MT" environment variable to '
                        'the root installation of minitage or use the minitage.instance.env template '
                        'and source the resulting environment file before launching cgwb<br/>'
                        '<p>You can generate one with:</p><br/>'
                        '<pre>\n'
                        '\t$minitage/bin/easy_install -U minitage.paste\n'
                        '\t$minitage/bin/paster create -t minitage.instances.env cgwb-dev (or cgwb)'
                        '</pre>'
                        '<br/><p>And before launching cgwb, if you do not have done that previously in your running shell:</p><br/>'
                        '<pre>\n'
                        '\tsource $minitage/bfg/cgwb(-dev)/sys/share/minitage/minitage.env'
                        '</pre>'
                        '</li></ul><br/>'
                        '' % (action, e) 
                    ) 
                except Parser.ParseError, e:
                    errors.append(
                        '<div class="error">'
                        '<p>%s/ Error while reading paster variables:</p>'
                        '<p class="pythonerror">%r</p>'
                        '<p class="pythonerror"><pre>%s</pre></p>' 
                        '</div>'% (action, e, e.report())
                    ) 
                except Exception, e:
                    errors.append(
                        '<div class="error">'
                        '<p>%s/ Error while reading paster variables:</p>'
                        '<p class="pythonerror">%r</p>'
                        '<p class="pythonerror">%s</p>' 
                        '</div>'% (action, e, e)
                    )
    main = get_template('templates/main_template.pt')

    return render_template_to_response(
        'templates/process.pt',
        request = request,
        errors = errors,
        context=context,
        output=output_dir_prefix,
        download_path=download_path,
        main=main)



def webbuilder_collectinformation(context, request):
    errors, added_options = [], []
    paster, default_group_data, templates_data = None, None, None
    try:
        paster = get_paster(context.configuration)
        templates_data = paster.templates_data
        added_options = paster.added_options
    except NoSuchConfigurationError:
        errors.append('The required configuration does not exists : %s' % context.configuration)
    except Exception, e:
        raise
        errors.append('Error while reading paster variables: <pre>%r</pre>'%e)
    main = get_template('templates/main_template.pt')

    return render_template_to_response(
        'templates/collect.pt',
        request = request,
        errors = errors,
        context=context,
        main=main,
        templates = templates_data,
        get_value=get_value)

def get_value(template, aliasname, default=None):
    res = default
    if aliasname:
        for var, alias, default in template['aliases']:
            # we have a value
            if aliasname == alias:
                res = default
    return res
     
