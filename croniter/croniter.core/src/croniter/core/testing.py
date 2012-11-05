
def print_contents(browser, dest='~/.browser.html'):
    """Print the browser contents somewhere for you to see its context
    in doctest pdb, type print_contents(browser) and that's it, open firefox
    with file://~/browser.html."""
    import os
    open(os.path.expanduser(dest), 'w').write(browser.contents)


from plone.testing.layer import Layer as Base

class Layer(Base):

    defaultBases = tuple()

class IntegrationLayer(Layer):
    """."""

class FunctionnalLayer(IntegrationLayer):
    """."""
                                  

CRONITER_CORE_FIXTURE = Layer()
CRONITER_CORE_INTEGRATION_TESTING = IntegrationLayer()
CRONITER_CORE_FUNCTIONAL_TESTING = FunctionnalLayer()
