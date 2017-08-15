''' application.py: Web Application '''

from .handler import CodeHandler, QuizHandler

import logging
import os

import tornado.ioloop
import tornado.web

# Dredd Constants -------------------------------------------------------------

DREDD_ADDRESS  = '0.0.0.0'
DREDD_PORT     = 9206
DREDD_ASSETS   = os.path.join(os.path.dirname(__file__), 'assets')
DREDD_DATA_DIR = 'data'

# Dredd Application -----------------------------------------------------------

class Application(tornado.web.Application):

    def __init__(self, **settings):
        tornado.web.Application.__init__(self, **settings)

        self.logger   = logging.getLogger()
        self.address  = settings.get('address', DREDD_ADDRESS)
        self.port     = settings.get('port', DREDD_PORT)
        self.ioloop   = tornado.ioloop.IOLoop.instance()
        self.data_dir = DREDD_DATA_DIR

        self.add_handlers('.*', [
            (r'.*/assets/(.*)', tornado.web.StaticFileHandler, {'path', DREDD_ASSETS}),
            (r'.*/code/(.*)'  , CodeHandler),
            (r'.*/quiz/(.*)'  , QuizHandler),
        ])

    def run(self):
        try:
            self.listen(self.port, self.address)
        except socket.error as e:
            self.logger.fatal('Unable to listen on {}:{} = {}'.format(self.address, self.port, e))
            sys.exit(1)

        self.ioloop.start()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
