import re

import pkg_resources

from zope.interface import implements

from collective.generic.webbuilder import interfaces
from collective.generic.webbuilder.models import root

class NoSuchConfigurationError(Exception): pass
class PasterAssembly(object):
    implements(interfaces.IPasterAssembly)
    def __init__(self, configuration):
        try:
            self.configuration = root.configurations[configuration]
        except KeyError:
            raise NoSuchConfigurationError(configuration)
        self.configuration_name = configuration
        self.templates_data = []
        self.added_options = []

class PasterAssemblyReader(object):
    implements(interfaces.IPasterAssemblyReader)

    def __init__(self, paster):
        self.paster = paster
        self.readed= False

    def read(self):
        if self.readed: return
        p = self.paster
        configuration = self.paster.configuration
        templates = configuration.templates.values()
        templates.sort(lambda x,y: x.order - y.order)
        for template in templates:
            not_explicit_options = {}
            default_group = None
            groups_data = []
            template_data = {'self': template,
                             'name': template.name,
                             'groups': groups_data,
                             'aliases' : [],
                             'template': None,
                             'added_options': [],
                             'display': False,
                             'not_explicit_options': not_explicit_options
                            }
            p.templates_data.append(template_data)
            groups = template.groups.values()
            groups.sort(lambda x,y: x.order-y.order)
            dgd = None
            for group in groups:
                gd = {'name': group.name, 'group': group,  'options': []}
                if group.name == 'default':
                    default_group = group
                    dgd = gd
                groups_data.append(gd)
            eps = [a
                   for a in pkg_resources.iter_entry_points('paste.paster_create_template',
                                                            template.name)]
            if eps:
                ep = eps[0].load()
                template_data['template'] = ep
                for var in ep.vars:
                    skip = False
                    for opt in default_group.exclude_options:
                        if opt == var.name:
                            skip = True
                    for opt in default_group.excludes_options:
                        if re.match(opt, var.name):
                            skip = True
                    for group_data in groups_data:
                        if group_data['name'] != 'default' and not skip:
                            group, found, option = group_data['group'], False, None
                            for soption in group.single_options:
                                option = group.single_options[soption]
                                if option.name == var.name:
                                    found = True
                                    break
                            if not found:
                                for soption in group.options:
                                    option = group.options[soption]
                                    if re.match(option.prefix, var.name):
                                        found = True
                                        break
                            if not found and not var in template_data['added_options']:
                                not_explicit_options[var.name] = (var, 'default', None, None)
                                option = None
                            if found and option:
                                type =  getattr(option, 'type', '')
                                if not type:
                                    type = 'default'
                                alias = getattr(option, 'alias', None)
                                name = var.name
                                if option.default:
                                    var.default = option.default
                                    for b in ['true', 'y', 'on']:
                                        if option.default.startswith(b):
                                            type = 'boolean'
                                if alias:
                                    template_data['aliases'].append((var, alias, var.default))
                                option.type = type
                                if ((not name in p.added_options)
                                    and (not name in template_data['added_options'])
                                   ) or alias:
                                    if not alias or (alias and (not alias in p.added_options)):
                                        group_data['options'].append((var, option.type, alias, option))
                                        template_data['added_options'].append(name)
                                        # add the option globally only and only if the option is not aliased
                                        if not alias:
                                            p.added_options.append(name)
                                        if alias:
                                            p.added_options.append(alias) 
                                        # first option added which is not hidden
                                        # will make the template display
                                        if not option.type == 'hidden':
                                            template_data['display'] = True
                        # after each group parsing, look if we have matched
                        # a previous non-matched option.
                        for name in p.added_options + template_data['added_options']:
                            if name in not_explicit_options:
                                del not_explicit_options[name]
                    # after all groups had been parsed, just mark the default options as added
                    for name in not_explicit_options:
                        dgd['options'].append(not_explicit_options[name])
                        template_data['added_options'].append(name)
                        p.added_options.append(name)
        self.readed = True



