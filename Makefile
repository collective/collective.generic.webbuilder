#
# Makefile for javascript resources
#
PATH_BASE=$(PWD)
PATH_RESOURCES_TARGET=$(PATH_BASE)/src/collective/generic/webbuilder/templates
PATH := $(PWD)/node_modules/.bin:$(PWD)/bin:$(PATH)
B=node_modules/.bin/

all: buildout resources
all-production: prod resources

$(B)/buildout:
	python bootstrap.py

bin/npm: bin/buildout
	bin/buildout install nodejs

npm_install:
	npm install -d

$(B)/bower: npm_install

$(B)/gulp: npm_install

resources: $(B)/bower $(B)/gulp  bin/npm
	echo $$PATH
	npm install
	bower install
	gulp

watch: resources
	bin/grunt watch

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
