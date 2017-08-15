#!/usr/bin/env python2.7

import os
import sys

sys.path.append(os.curdir)

from dredd.application import Application, DREDD_PORT

import tornado.options

# Main Execution --------------------------------------------------------------

if __name__ == '__main__':
    tornado.options.define('debug', default=False, help='Enable debugging mode.')
    tornado.options.define('port', default=DREDD_PORT, help='Port to listen on.')
    tornado.options.parse_command_line()

    options = tornado.options.options.as_dict()
    dredd   = Application(**options)
    dredd.run()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
