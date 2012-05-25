#!/usr/bin/env bash


cd $(dirname $0)
envf=sys/share/minitage/minitage.env 
if [ -f $envf ];then
    . $envf
fi
reset;./bin/cgwb --port=8081 --reload
# vim:set et sts=4 ts=4 tw=80:
