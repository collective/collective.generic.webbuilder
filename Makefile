PATH_BASE=$(PWD)
PATH_RESOURCES_TARGET=$(PATH_BASE)/src/collective/generic/webbuilder/templates

NPM=npm
GRUNT=grunt
BOWER=bower

all: buildout resources
all-production: prod resources

resources:
	cd $(PATH_RESOURCES_TARGET)/static_dev; $(NPM) install; $(BOWER) install; $(GRUNT)

watch:
	cd $(PATH_RESOURCES_TARGET)/static_dev; $(GRUNT) watch

buildout:
	bin/buildout

openshift:
	bin/buildout -c openshift.cfg

prod:
	bin/buildout -c production.cfg

clean-buildout:
	rm -rf bin buildout-cache parts

clean-resources:
	rm -rf $(PATH_RESOURCES_TARGET)/static_dev/node_modules
	rm -rf $(PATH_RESOURCES_TARGET)/static_dev/bower_components
	rm -rf $(PATH_RESOURCES_TARGET)/static

clean: clean-buildout clean-resources
