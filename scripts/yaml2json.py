#!/usr/bin/python3

import json
import sys

import yaml

print json.dumps(yaml.safe_load(sys.stdin), indent=4)
