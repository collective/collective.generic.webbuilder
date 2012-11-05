import logging
from zope.i18nmessageid import MessageFactory
MessageFactory = foobarmyothereggMessageFactory = MessageFactory('foo.bar.myotheregg') 
logger = logging.getLogger('foo.bar.myotheregg')
def initialize(context):
    """Initializer called when used as a Zope 2 product.""" 
