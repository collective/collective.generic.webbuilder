import sys
import ConfigParser
import os.path
import random
import socket
import threading

from paste.deploy import loadapp
from paste.httpserver import serve

# if you have plone.reload out there add an helper to use in doctests while programming
# just use preload(module) in pdb :)
# it would be neccessary for you to precise each module to reload, this method is also not recursive.
# eg: (pdb) from foo import bar;preload(bar)
try:
    def preload(modules_or_module, excludelist=None):
        modules = modules_or_module
        if not (isinstance(modules_or_module, list)
                or isinstance(modules_or_module, tuple)):
            modules = [modules_or_module]
        if not excludelist:
            excludelist = []
        import sys
        if not modules:
            modules = sys.modules
        from plone.reload.xreload import Reloader
        print modules
        for module in modules:
            if not module in excludelist:
                try:
                    Reloader(module).reload()
                except Exception, e:
                    pass
except:
    pass

def get_interfaces(o):
    return [o for o in o.__provides__.interfaces()]
try:from zope.interface import implementedBy, providedBy
except:pass

# used on testing
# copied from ZopeLite Class from zope.testingZope.TestCase
# but we can't import it
# if we do we polluate our os.environment and ZopeTestcase usecase detction
def _print(msg):
    '''Writes 'msg' to stderr and flushes the stream.'''
    sys.stderr.write(msg)
    sys.stderr.flush()

try:
    import zope
    from zope.traversing.adapters import DefaultTraversable
    zope.component.provideAdapter(DefaultTraversable, [None])
    class Request(zope.publisher.browser.TestRequest):
        def __setitem__(self, name, value):
            self._environ[name] = value
    # alias
    TestRequest = Request
    def make_request(url='http://nohost/@@myview',form=None, *args,  **kwargs):
        r = Request(environ = {'SERVER_URL': url, 'ACTUAL_URL': url}, form=form, *args, **kwargs)
        zope.interface.alsoProvides(r, zope.annotation.interfaces.IAttributeAnnotatable)
        return r
except Exception, e:pass

def pstriplist(s):
    print '\n'.join([a.rstrip() for a in s.split('\n') if a.strip()])


here_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def getApp():
    wsgiapp = loadapp('config:cgwb.ini', relative_to = here_dir)
    return wsgiapp

def get_port():
    for i in range(30):
        port = random.randrange(20000, 30000)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            try:
                s.connect(('localhost', port))
            except socket.error:
                return port
        finally:
            s.close()
    raise RuntimeError, "Can't find port"

class BFGServer:
    #def testSetUp(self, *args, **kwargs):
    def launch(self, app=None, host = '0.0.0.0'):
        """
        Some instance are registred there
            - server: wsgi server
            - host: wsgi server host
            - port: wsgi server port
            - app: the Pylon wsgi application
            - t: the thread where the server is running in
        """
        if not app: app = getApp()
        self.app = app
        self.host = host
        self.port = get_port()
        self.server = serve(self.app,
                            self.host, self.port,
                            socket_timeout=1,
                            start_loop=False,
                           )
        def server_close(self):
            """
            Finish pending requests and shutdown the server.
            """
            self.running = False
            self.socket.close()
            self.thread_pool.shutdown(1)

        def mainloop():
            """Handle requests."""
            self.server.server_close = server_close
            self.server.serve_forever()
        self.t = threading.Thread(target=mainloop)
        self.t.setDaemon(False)
        self.t.start()

    def get_url(self):
        return 'http://%s:%s/' % (self.host, self.port)

    def tearDown(self):
        self.server.server_close(self.server)
        self.t.join()

_LAUNCHED_SERVERS = []
def launch_server():
    server = BFGServer()
    server.launch()
    _LAUNCHED_SERVERS.append(server)
    return server, server.get_url()

