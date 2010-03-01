import re

from zope.interface import Interface, implements

re_flags = re.M|re.U|re.I|re.S

class IWebBuilder(Interface):
    """."""

class WebBuilder(object):
    implements(IWebBuilder)
    configurations = {}

class Data(object):
    def __init__(self, environ):
        self.__dict__.update(environ['bfg.routes.matchdict'])
    def compute_value(self, value):
        if not value:
            return False
        value = value.strip().lower()
        if value == 'n':
            return False
        for b in 'off', 'false':
            if value.startswith(b):
                return False
        return True
    def get_id(self, value):
        special_chars = ['.', '_', '-', ' ']
        for c in special_chars:
            value = value.replace(c, '')
        return value

    def rewrite_description(self, value):
        url = re.compile('(?P<url>(?<!>)(?<!href=[\'"])https?\:\//[^$\s"]*)',re_flags)
        yn = re.compile('y/n\s*[?]?$',re_flags)
        see = re.compile(',\s*see\s*(ht.*)$',re_flags)
        if yn.search(value):
            value = yn.sub('', value)
        if see.search(value):
            value = see.sub('\\1', value)
        match_obj = url.search(value)
        while match_obj:
            durl = match_obj.groupdict()
            value = value.replace( durl['url'], '')
            value =  "%s%s" % (
                value,
                '<a class="option-desc-url" target="_blank" '
                'href="%(url)s"     '
                'alt="link">&nbsp;</a>' % durl
            )
            match_obj = url.search(value)
        return value.strip()

root = WebBuilder()
def get_root(environ):
    return root

