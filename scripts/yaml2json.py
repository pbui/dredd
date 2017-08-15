#!/usr/bin/python2.7

import json
import sys

import yaml

print json.dumps(yaml.load(sys.stdin), indent=4)
