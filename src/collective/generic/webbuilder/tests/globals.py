#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################################
# ADD GLOBALS TO BE USED Inside your doctests there
##########################################################################################

import os
import re
from copy import deepcopy
from pprint import pprint  

from zope.configuration import xmlconfig
from StringIO import StringIO
cwd = os.path.dirname(__file__)
import pkg_resources
try:
    from Products.Five.testbrowser import Browser
    browser = Browser()
except:pass
try:import zope
except:pass
try:from zope.interface.verify import verifyObject
except:pass  
try:import collective
except:pass
try:from zope import interface, schema
except:pass
try:from zope.component import adapts, getMultiAdapter, getAdapter, getAdapters
except:pass 
try:import z3c
except:pass 
try:from five import grok
except:pass  
try:from five.grok.testing import grok as fgrok
except:pass   
try:from Products.statusmessages.interfaces import IStatusMessage
except:pass
try:from Acquisition import aq_inner, aq_parent, aq_self, aq_explicit
except:pass

from collective.generic.webbuilder import interfaces
from collective.generic.webbuilder.models import root
from collective.generic.webbuilder import paster as gpaster

zcmlContext = None
def _callFUT(name, package=None, context = None):
    if not context: context = zcmlContext
    result = xmlconfig.file(
        context = context,
        name = name, 
        package = package
    )
    return result

from collective.generic.webbuilder.tests.utils import launch_server

from zope.testbrowser.browser import Browser
from lxml.html import fromstring as htmlS


