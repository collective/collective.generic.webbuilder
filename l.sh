#!/usr/bin/env bash
cd $(dirname $0)
reset;./bin/pserve --reload etc/cgwb.ini
# vim:set et sts=4 ts=4 tw=80:
