import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = collectivecronMessageFactory = MessageFactory('collective.cron') 
logger = logging.getLogger('collective.cron')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
