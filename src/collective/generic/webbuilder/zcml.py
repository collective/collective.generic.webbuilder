from zope.interface import Interface, implements
from zope import schema
from zope import component
from zope.configuration.config import GroupingContextDecorator
from collective.generic.webbuilder.models import root

gsm = component.getGlobalSiteManager()

class IPasterConfiguration(Interface):
    name =  schema.BytesLine(title=u"name", description=u"This is a configuration of paster templates", required=True)
    templates = schema.Dict(title=u"templates",)
    plugins = schema.List(title=u"plugins",)

class ITemplate(Interface):
    name =  schema.BytesLine(title=u"Pasters assembly", description=u"This is a configuration of paster templates", required=True)
    order = schema.Int( title=u"template generation order", description=u"The template generation order", required=True)
    output = schema.Int( title=u"template generation folder", description=u"The template generation folder", required=False)
    groups = schema.List(title=u"groups",)

class IGroup(Interface):
    name =  schema.BytesLine(title=u"Pasters assembly", description=u"This is a configuration of paster templates", required=True)
    order = schema.Int( title=u"template generation order", description=u"The group display order", required=True)
    options = schema.List(title=u"options",)
    single_options = schema.List(title=u"single options",)
    exclude_options = schema.List(title=u"exclude options",)

class IOption(Interface):
    name =  schema.BytesLine(title=u"option", description=u"This is an option", required=True)
    type =  schema.BytesLine(title=u"Options type", description=u"This is options type", required=False)
    default =  schema.BytesLine(title=u"Options default", description=u"This is options default", required=False)
    alias =  schema.BytesLine(title=u"Option alias", description=u"This is option alias for conflict handling", required=False)

class IOptions(Interface):
    prefix =  schema.BytesLine(title=u"option", description=u"This is an option", required=True)
    type =  schema.BytesLine(title=u"Options type", description=u"This is options type", required=False)
    default =  schema.BytesLine(title=u"Options default", description=u"This is options default", required=False)

class IExcludeOption(Interface):
    name =  schema.BytesLine(title=u"option", description=u"This is an option", required=True)

class PasterConfiguration(GroupingContextDecorator):
    implements(IPasterConfiguration)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.name = kwargs['name']
        self.templates = {}
        self.plugins = []

    def after(self, **kwargs):
        root.configurations[self.name] = self

class Template(GroupingContextDecorator):
    implements(ITemplate)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        context.templates[kwargs['name']] = self
        self.name = kwargs['name']
        self.order = kwargs.get('order', None)
        self.output = kwargs.get('output', None)
        self.groups = {}
        Group(self, **{'name':'default', 'order': 9999999})

class Group(GroupingContextDecorator):
    implements(IGroup)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.name = kwargs['name']
        self.order = kwargs.get('order', None)
        context.groups[kwargs['name']] = self
        self.single_options = {}
        self.options = {}
        self.exclude_options = {}
        self.excludes_options = {}

class ExcludeOption(GroupingContextDecorator):
    implements(IExcludeOption)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.name = kwargs['name']
        self.type = kwargs.get('type', '')
        self.context.groups['default'].exclude_options[self.name] = self

class ExcludeOptions(GroupingContextDecorator):
    implements(IExcludeOption)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.prefix = kwargs['prefix']
        self.context.groups['default'].excludes_options[self.prefix] = self

class Option(GroupingContextDecorator):
    implements(IOption)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.name = kwargs['name']
        self.type = kwargs.get('type', None)
        self.default = kwargs.get('default', None)
        self.context.single_options[self.name] = self

class Options(GroupingContextDecorator):
    implements(IOption)
    def __init__(self, context, *args, **kwargs):
        GroupingContextDecorator.__init__(self, context, *args, **kwargs)
        self.prefix = kwargs['prefix']
        self.type = kwargs.get('type', None)
        self.default = kwargs.get('default', None)
        self.context.options[self.prefix] = self

class IGenericPasterDirective(Interface):
    name = schema.BytesLine(title=u"Pasters assembly", description=u"This is a configuration of paster templates", required=True)

def GenericPaster_handler(context, *args, **kwargs):
    return PasterConfiguration(context, **kwargs)

class ITemplateDirective(Interface):
    name = schema.BytesLine(title=u"Pasters assembly", description=u"This is a configuration of paster templates", required=True)
    order = schema.Int(title=u"template generation order", description=u"The template generation order", required=True)
    output = schema.BytesLine(title=u"template generation folder", description=u"The template generation folder", required=False)

def Template_handler(context, *args, **kwargs):
    return Template(context, **kwargs)

class IGroupDirective(Interface):
    name = schema.BytesLine(title=u"Pasters assembly", description=u"This is a configuration of paster templates", required=True)
    order = schema.Int(title=u"group display order", description=u"The group display order", required=False)

def Group_handler(context, *args, **kwargs):
    return Group(context, **kwargs)

class IOptionsDirective(Interface):
    type = schema.BytesLine(title=u"Options type", description=u"This is  options type", required=False)
    prefix = schema.BytesLine(title=u"Options to include", description=u"This are options", required=True)
    default = schema.BytesLine(title=u"Options default", description=u"This are options default value", required=False)

def Options_handler(context, *args, **kwargs):
    return Options(context, **kwargs)

class IOptionDirective(Interface):
    name = schema.BytesLine(title=u"option", description=u"This is an option", required=True)
    type = schema.BytesLine(title=u"Options type", description=u"This is  options type", required=False)
    default = schema.BytesLine(title=u"Options default", description=u"This is options default", required=False)
    alias = schema.BytesLine(title=u"alias", description=u"Alias for option if it conflicts with another one", required=False)

def Option_handler(context, *args, **kwargs):
    return Option(context, **kwargs)

class IExcludeOptionDirective(Interface):
    name = schema.BytesLine( title=u"exclude option", description=u"this is an option to exclude", required=True)

def ExcludeOption_handler(context, *args, **kwargs):
    return ExcludeOption(context, **kwargs)

class IExcludeOptionsDirective(Interface):
    prefix = schema.BytesLine( title=u"exclude option", description=u"this is an option to exclude", required=True)

def ExcludeOptions_handler(context, *args, **kwargs):
    return ExcludeOptions(context, **kwargs)

class IPluginDirective(Interface):
    name = schema.BytesLine( title=u"plugin name", description=u"this is a plugin name to execute if found", required=True)
    order = schema.Int(title=u"plugin order", description=u"The plugin order", required=False)

def Plugin_handler(context, *args, **kwargs):
    context.plugins.append((kwargs['name'], kwargs['order']))
    return context



