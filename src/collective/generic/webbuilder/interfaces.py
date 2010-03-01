#!/usr/bin/env python

# Copyright (C) 2009, Mathieu PASQUET <mpa@makina-corpus.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the <ORGANIZATION> nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__docformat__ = 'restructuredtext en'

from zope.interface.interface import adapter_hooks
from zope.interface import Interface, Attribute
from zope import component

def hook(provided, object, name=''):
    adapter = component.getAdapter(object, provided, name=name)
    return adapter(object)
adapter_hooks.append(hook)

class IPostGenerationPlugin(Interface):
    """Run after all paster have ran
    you must also register the name of your plugin inside the
    zcml declation of your configuration with <plugin name="foo" order="1"/>
    """
    name = Attribute("name")
    order = Attribute("order")
    def process(output_dir, project_name, params):
        """."""

class IPasterAssembly(Interface):
    """describe an assembly of pasters."""
    configuration = Attribute('configuration')
    configuration_name = Attribute('configuration name')
    template_data = Attribute('template data')
    added_options = Attribute('added options')

class IPasterAssemblyReader(Interface):
    """."""
    def read():
        """Read the assemble and return a
        dict of infos found inside (groups, options)."""


# vim:set et sts=4 ts=4 tw=80:
