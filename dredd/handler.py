''' handler.py: Web Handlers '''

from .quiz import Quiz

import json
import os

import tornado.web

# Quiz Handler ----------------------------------------------------------------

class QuizHandler(tornado.web.RequestHandler):

    def get(self, quiz_name):
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        try:
            quiz = Quiz(os.path.join(self.application.data_dir, 'quiz', quiz_name))
        except IOError as e:
            return self.error(404, str(e))

        self.write(json.dumps(quiz.questions))

    def post(self, quiz_name):
        try:
            quiz = Quiz(os.path.join(self.application.data_dir, 'quiz', quiz_name))
        except IOError as e:
            return self.error(404, str(e))

        try:
            responses = json.loads(self.request.body)
        except ValueError as e:
            return self.error(400, 'Unable to parse request body: {}'.format(e))

        try:
            self.write(json.dumps(quiz.evaluate(responses)))
        except Exception as e:
            return self.error(400, 'Unable to evaluate response: {}'.format(e))

    def error(self, status_code, error_message):
        self.clear()
        self.set_status(status_code)
        self.write(json.dumps({
            'status': status_code,
            'error' : error_message,
        }))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
