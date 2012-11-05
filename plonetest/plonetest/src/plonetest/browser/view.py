#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Acquisition import aq_parent
from Acquisition import aq_parent


class IMyView(interface.Interface):
    """Marker interface"""


class MyView(BrowserView):
    """MY view doc"""
    interface.implements(IMyView)
    template = ViewPageTemplateFile('template.pt')
    def __call__(self, **params):
        """."""
        params = {}
        return self.template(**params)

# vim:set et sts=4 ts=4 tw=80:

