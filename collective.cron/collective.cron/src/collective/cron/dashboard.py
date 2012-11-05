from zope.interface import implements
from zope.component import adapts
from interfaces import IMyPortalUser
from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.portlets import portlets

class MyPortalDefaultDashboard(DefaultDashboard):
    """ A new custom default dashboard for users. """
    implements(IDefaultDashboard)
    adapts(IMyPortalUser)

    def __call__(self):
        d1, d2, d3, d4 = [], [], [], []
        #d1.append(portlets.recent.Assignment())

        return {
            'plone.dashboard1' : d1,
            'plone.dashboard2' : d2,
            'plone.dashboard3' : d3,
            'plone.dashboard4' : d4,
        }
