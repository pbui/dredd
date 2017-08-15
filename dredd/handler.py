''' handler.py: Web Handlers '''

from .quiz import Quiz

import json
import os
import shlex
import shutil
import tempfile

import tornado.gen
import tornado.process
import tornado.web

# Code Handler ----------------------------------------------------------------

class CodeHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self, code_name):
        try:
            # Create sandbox
            try:
                sandbox = tempfile.mkdtemp()
            except OSError as e:
                self.error(500, 'Unable to create sandbox: {}'.format(e))

            # Copy input and output to sandbox
            input_src  = os.path.join(self.application.data_dir, 'code', code_name, 'input.txt')
            input_dst  = os.path.join(sandbox, 'input.txt')
            output_src = os.path.join(self.application.data_dir, 'code', code_name, 'output.txt')
            output_dst = os.path.join(sandbox, 'output.txt')

            try:
                shutil.copyfile(input_src, input_dst)
                shutil.copyfile(output_src, output_dst)
            except OSError as e:
                self.error(404, 'Unable to copy input and output files: {}'.format(e))

            # Write source to sandbox
            source = self.request.files['source'][0]

            try:
                with open(os.path.join(sandbox, source['filename']), 'w') as fs:
                    fs.write(source['body'])
            except IOError as e:
                self.error(500, 'Unable to copy source code: {}'.format(e))

            # Execute runner
            command = 'scripts/sandbox.sh {} scripts/run.py {} {} {}'.format(
                sandbox, source['filename'], 'input.txt', 'output.txt'
            )

            process = tornado.process.Subprocess(shlex.split(command), stdout=tornado.process.Subprocess.STREAM)
            result  = yield tornado.gen.Task(process.stdout.read_until_close)

            # Write results
            self.write(result)

        except Exception as e:
            self.error(400, 'Unable to execute code: {}'.format(e))

        finally:
            shutil.rmtree(sandbox)

    def error(self, status_code, error_message):
        self.clear()
        self.set_status(status_code)
        self.write(json.dumps({
            'status': status_code,
            'error' : error_message,
        }))

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
