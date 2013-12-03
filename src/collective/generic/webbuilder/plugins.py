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

import os
import sys
import re

re_flags = re.M|re.U|re.I|re.S

from zope.interface import implements
from collective.generic.webbuilder import interfaces
from iniparse import INIConfig

from collective.generic.webbuilder.utils import remove_path

class DummyPlugin(object):
    implements(interfaces.IPostGenerationPlugin)

    def __init__(self, paster):
        self.paster = paster

    def process(self, output_dir):
        print "I am a dummy plugin doing nothing inside %s for %s" % (
            output_dir,
            self.paster.configuration.name
        )


def remove_egg_info(p):
    for dirpath, dirnames, filenames in os.walk(p):
        for filename in dirnames+filenames:
            if 'egg-info' in filename:
                remove_path(
                    os.path.join(dirpath, filename)
                )
        for directory in dirnames:
            subdir = os.path.join(dirpath, directory)
            remove_egg_info(subdir)

class EggInfoPlugin(DummyPlugin):

    def process(self, output_dir, project_name, params):
        remove_egg_info(output_dir)

class EggPlugin(DummyPlugin):

    def process(self, output_dir, project_name, params):
        """."""
        eggsnames = []
        devnames = []
        src_dir = os.path.join(output_dir, 'src')
        for path in os.listdir(src_dir):
            p = os.path.join(src_dir, path)
            if os.path.isdir(p):
                if os.path.exists(os.path.join(p, 'setup.py')):
                    eggsnames.append(path)
                    devnames.append(os.path.join('src', path))
        zcmlnames = [n
                     for n in eggsnames
                     if (('policy' in n)
                         or (n==project_name)
                         or (n=='%s.core' % project_name)
                        )]

        f = os.path.join(output_dir, 'buildout.cfg')
        sf = os.path.join(
            output_dir, 'etc', 'project', 'sources.cfg')
        pf = os.path.join(output_dir,
                         'etc', 'project',
                         '%s.cfg' % project_name
                        )
        if os.path.exists(pf):
            f = pf
        else:
            for i in ['django', 'plone', 'pyramid']:
                pf = os.path.join(output_dir,
                                  'etc', 'project',
                                  '%s.cfg' % i
                                 )
                if os.path.exists(pf):
                    f = pf
        cfg = INIConfig(open(f))
        srccfg = None
        if os.path.exists(sf):
            srccfg = INIConfig(open(sf))
        else:
            srccfg = cfg

        extdevoption_re  = re.compile('develop\s*\+\s*', re_flags)
        devoption_re     = re.compile('develop\s*', re_flags)
        autocheckout_option_re     = re.compile(
            'auto-checkout\s*', re_flags)
        ext_autocheckout_option_re     = re.compile(
            'auto-checkout\s*\+\s*', re_flags)
        exteggsoption_re = re.compile('eggs\s*\+\s*', re_flags)
        eggsoption_re    = re.compile('eggs\s*', re_flags)
        eggsoption_re    = re.compile('eggs\s*', re_flags)
        devoption, eggsoption= 'develop+', 'eggs+'
        autocheckout_option = 'autocheckout+'
        devfound, eggsfound, acfound = False, False, False
        for optionre in [ext_autocheckout_option_re,
                         autocheckout_option_re, ]:
            if 'buildout' in cfg:
                for option in cfg.buildout:
                    if optionre.match(option):
                        acfound = True
                        autocheckout = option
                        break
        for optionre in [extdevoption_re, devoption_re, ]:
            if 'buildout' in cfg:
                for option in cfg.buildout:
                    if optionre.match(option):
                        devfound = True
                        devoption = option
                        break

        for optionre in [exteggsoption_re, eggsoption_re, ]:
            for option in cfg.buildout:
                if optionre.match(option):
                    eggsfound = True
                    eggsoption = option
                    break

        if eggsfound:
            for eggn in eggsnames:
                if not (eggn in cfg.buildout[eggsoption]):
                    cfg.buildout[eggsoption] = '\n    '.join(
                        [a for a in eggn,
                         cfg.buildout[eggsoption].strip()
                         if a.strip()])
        else:
            cfg.buildout[eggsoption] = ''
            for eggn in eggsnames:
                cfg.buildout[eggsoption] = '\n    '.join(
                    [a for a in
                     eggn,
                     cfg.buildout[eggsoption].strip()
                     if a.strip()])
        if srccfg:
            if acfound:
                for eggn in eggsnames:
                    if 'sources-dir' in cfg.buildout:
                        del cfg.buildout['sources-dir']
                    if not (eggn in cfg.buildout[autocheckout]):
                        cfg.buildout[autocheckout] = '\n    '.join(
                            [a for a in
                             eggn,
                             cfg.buildout[autocheckout].strip()
                             if a.strip()])
                    if not (eggn in cfg.sources):
                        cfg.sources[eggn] = 'fs %s' % (eggn,)
                        cfg.sources._lines[0].contents.insert(
                            1, cfg.sources._lines[0].contents.pop(-1))
        else:
            if devfound:
                for eggn in devnames:
                    if not (eggn in cfg.buildout[devoption]):
                        cfg.buildout[devoption] = '\n    '.join(
                            [a for a in
                             eggn,
                             cfg.buildout[devoption].strip()
                             if a.strip()])
            else:
                cfg.buildout[devoption] = ''
                for eggn in devnames:
                    cfg.buildout[devoption] = '\n    '.join(
                        [a for a in eggn,
                         cfg.buildout[devoption].strip()
                         if a.strip()])

        # zcml are now handled via collective.generic.skel
        extzcmloption_re  = re.compile('zcml\s*\+\s*', re_flags)
        zcmloption_re     = re.compile('zcml\s*', re_flags)
        zcmlfound = False
        for optionre in [extzcmloption_re, zcmloption_re, ]:
            if 'buildout' in cfg:
                for option in cfg.buildout:
                    if optionre.match(option):
                        zcmlfound = True
                        zcmloption = option
                        break

        if zcmlfound:
            for eggn in zcmlnames:
                if 'buildout' in cfg:
                    if not (eggn in cfg.buildout[zcmloption]):
                        if (('policy' in eggn )
                            or ('tma' in eggn)
                            or ('.core' in eggn)
                            or (project_name == eggn)
                           ):
                            cfg.buildout[zcmloption] = '\n    '.join([
                                a for a in
                                cfg.buildout[zcmloption].strip(),
                                eggn if a.strip()])
        else:
            zcmloption = ''
            for eggn in zcmlnames:
                if 'instance' in cfg:
                    if 'policy' in eggn:
                        cfg.buildout[zcmloption] = '\n    ' % (
                            [a for a in eggn,
                            cfg.buildout[zcmloption].strip()
                            if a.strip()])
        f = open(f, 'w')
        cfg = '%s'%cfg
        cfg = cfg.replace('+ =', ' +=')
        f.write(cfg)
        f.close()

# plugin.process('/tmp/tmpRKqUZh')
# print open ( '%s/buildout.cfg' %'/tmp/tmpRKqUZh'  ).read()
# vim:set et sts=4 ts=4 tw=80:
