==========================
CWGB
==========================

CGWB is a web interface to ``paster``, its goal is to generate a webinterface for selection options for a set of templates.

Imagine that you have 2 templates, the one that can deploy an application, and the other which generates the application in itself.

Declaring the two templates as a ``cgwb set`` will make a webinterface for those 2 templates. Answering correctly to the questions will produce a tarball that you ll be able download and unpack to have your base installation setup.

To make the templates available, you must define the set using ZCML.


As this server was developped as a quick and efficient interface to paster, *it is not safe to open it to wide internet.*
For security reason, just launch/use when you need it.

Next versions will include some sessions/roles and improved security, it may be possible at this stage to leave it open.

