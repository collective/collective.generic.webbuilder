import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = plonetestMessageFactory = MessageFactory('plonetest') 
logger = logging.getLogger('plonetest')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
