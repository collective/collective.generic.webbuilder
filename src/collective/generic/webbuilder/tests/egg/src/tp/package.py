import sys
import os
import re

from paste.script.templates import var
from paste.script.templates import Template

from minitage.paste.common import boolify


class Package(Template):
    """
    Package template to do a double namespace egg.
    Althout it prentends to do that, it is a base for sub templates that need to have all sort
    of variables defined. That's why there is some curious plone bits there.
    """
    _template_dir = 'tmpl'
    summary = "Template1 for cgwb testing"
    egg_plugins = ['PasteScript',]
    use_cheetah = True
    vars = [
        var('namespace', 'Namespace', default='%(namespace)s'),
        var('nested_namespace', 'Nested Namespace', default='%(package)s'),
        var('version', 'Version', default='1.0'),
        var('author', 'Author', default = 'foo',),
        var('author_email', 'Email', default = '%s@%s' % ('bar', 'localhost')),
        var('tp1option', 'URL of homepage', default='http://python.org'),
        var('tp1option2', 'One-line description of the package', default='Project %s'),
        var('tp1option3', 'One-line description of the package', default='y'),
        var('keywords', 'Space-separated keywords/tags'),
        var('license_name', 'License name', default='GPL'),
        var('project_name', 'Project namespace name (to override the first given project name forced by some derivated templates, left empty in doubt)', default=''),
    ]

    def run(self, command, output_dir, vars):
        self.output_dir = output_dir
        self.boolify(vars)
        self.pre(command, output_dir, vars)
        # may we have register variables ?
        if self.output_dir:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            output_dir = self.output_dir
        if not os.path.isdir(output_dir):
            raise Exception('%s is not a directory' % output_dir)
        self.write_files(command, self.output_dir, vars)
        self.post(command, output_dir, vars)
        if not command.options.quiet:
            print "-" * 79
            print "The template has been generated in %s" % self.output_dir
            print "-" * 79

    def boolify(self, d, keys=None):
        return boolify(d, keys)

    def read_vars(self, command=None):
        vars = Template.read_vars(self, command)
        infos = {}
        project = ''
        if command:
            project = command.args[0]
        from paste.script import pluginlib
        self.module = self.__class__.__module__
        def wrap_egg_info_dir(c, n):
            print "%s" % (
                " Monkey patching egg_info_dir "
            )
            return None
        pluginlib.egg_info_dir = wrap_egg_info_dir
        return vars



