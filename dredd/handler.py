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

# Index Handler ---------------------------------------------------------------

class IndexHandler(tornado.web.RequestHandler):

    def get(self, path):
        self.set_header('Content-Type', 'text/plain; charset="utf-8"')
        self.write('''
                     _              _     _
                  __| |_ __ ___  __| | __| |
                 / _` | '__/ _ \/ _` |/ _` |
                | (_| | | |  __/ (_| | (_| |
                 \__,_|_|  \___|\__,_|\__,_|

Quiz:

    # Post either JSON or YAML answers file
    $ curl -d@answers.json https://dredd.h4x0r.space/quiz/$name

Code:

    # Post source code with appropriate extension
    $ curl -F source=@program.c https://dredd.h4x0r.space/code/$name

    Note: All code is executed and evaluated in an Ubuntu 22.04 Docker
    container (e.g pbui/dredd-code:20230522), which supports the following
    programming language run-times:

    - Python 3.10.6
    - GCC 11.3.0
    - OpenJDK 11.0.19
    - Ruby 3.0
    - Node.js 18.x
    - TypeScript 5.0
    - Golang 1.18
    - Bash 5.1
    - Guile 2.2
    - Rust 1.72
    - GHC 8.8.4
    - SBCL 2.1.11
    - Mono 6.8.0.105
    - Swift 5.8
    - OCaml 4.13.1
''')

# Code Handler ----------------------------------------------------------------

class CodeHandler(tornado.web.RequestHandler):

    ENV = None

    @tornado.gen.coroutine
    def post(self, code_name):
        try:
            # Create sandbox
            try:
                sandbox = tempfile.mkdtemp()
            except OSError as e:
                return self.error(500, 'Unable to create sandbox: {}'.format(e))

            # Copy input and output to sandbox
            with tempfile.NamedTemporaryFile(dir=sandbox, delete=False) as tf:
                input_src  = os.path.join(self.application.data_dir, 'code', code_name, 'input.txt')
                input_dst  = tf.name

            with tempfile.NamedTemporaryFile(dir=sandbox, delete=False) as tf:
                output_src = os.path.join(self.application.data_dir, 'code', code_name, 'output.txt')
                output_dst = tf.name

            try:
                shutil.copyfile(input_src, input_dst)
                shutil.copyfile(output_src, output_dst)
            except OSError as e:
                return self.error(404, 'Unable to copy input and output files: {}'.format(e))

            # Write source to sandbox
            source = self.request.files['source'][0]

            try:
                with open(os.path.join(sandbox, source['filename']), 'wb') as fs:
                    fs.write(source['body'])
            except IOError as e:
                return self.error(500, 'Unable to copy source code: {}'.format(e))

            # Execute runner
            command = 'scripts/sandbox.sh {} scripts/run.py {} {} {}'.format(
                sandbox, source['filename'], os.path.basename(input_dst), os.path.basename(output_dst)
            )

            stream  = tornado.process.Subprocess.STREAM
            process = tornado.process.Subprocess(shlex.split(command), stdout=stream, env=self.ENV)
            result  = yield process.stdout.read_until_close()

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

# Debug Handler ---------------------------------------------------------------

class DebugHandler(CodeHandler):
    ENV = {'DEBUG': '1'}

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
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
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
