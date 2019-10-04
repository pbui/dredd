#!/usr/bin/env python3

import collections
import getopt
import itertools
import json
import logging
import os
import signal
import subprocess
import sys
import time

from subprocess import DEVNULL

# Constants --------------------------------------------------------------------

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

COMPILER_ERROR     = 1
EXECUTION_ERROR    = 2
WRONG_ANSWER       = 3
TIMELIMIT_EXCEEDED = 4
WRONG_FORMATTING   = 5
PROGRAM_SUCCESS    = 6

# Globals ----------------------------------------------------------------------

Logger = logging.getLogger()

# Functions --------------------------------------------------------------------

def usage(exit_code=0):
    print('''Usage: run [-d SANDBOX] [-t SECONDS -v] source input output

Options:

    -t SECONDS  Timeout duration before killing command (default is 10 seconds)
    -v          Display verbose debugging output
''', file=sys.stderr)
    sys.exit(exit_code)

# Languages --------------------------------------------------------------------

LanguageFields = 'name compile execute extensions'.split()
Language       = collections.namedtuple('Language', LanguageFields)

LANGUAGES = (
    Language('Bash',
        '',
        'bash {source}',
        ('.sh',)
    ),
    Language('C',
        'gcc -std=gnu99 -o {executable} {source} -lm',
        './{executable}',
        ('.c',)
    ),
    Language('C++',
        'g++ -std=gnu++11 -o {executable} {source} -lm',
        './{executable}',
        ('.cc', '.cpp')
    ),
    Language('Go',
        'go build {source}',
        'go run {source}',
        ('.go',)
    ),
    Language('Guile',
        '',
        'guile -s {source}',
        ('.scm',)
    ),
    Language('Java',
        'javac {source}',
        'java -cp . {executable}',
        ('.java',)
    ),
    Language('JavaScript',
        '',
        'nodejs {source}'
        , ('.js',)
    ),
    Language('Perl6',
        '',
        'perl6 {source}',
        ('.pl', '.p6')
    ),
    Language('Python',
        '',
        'python3 {source}',
        ('.py',)
    ),
    Language('Ruby',
        '',
        'ruby {source}',
        ('.rb',)
    ),
    Language('Rust',
        'rustc {source}',
        './{executable}',
        ('.rs',)
    ),
    Language('PHP 7.2',
        '',
        'php -f {executable}',
        ('.php',)
    ),
)

def get_language_from_source(source, language_name=None):
    extension = os.path.splitext(source)[-1]

    for language in LANGUAGES:
        matches_extension = extension in language.extensions
        matches_language  = language_name and language_name.lower() == language.name.lower()

        if matches_extension or matches_language:
            return language

    raise NotImplementedError

# Command ----------------------------------------------------------------------

def return_result(language, result, status=EXIT_FAILURE, score=COMPILER_ERROR, elapsed_time=0, output_path=None):
    data = {'result': result, 'score': score, 'time': elapsed_time}
    if int(os.environ.get('DEBUG', 0)) == 1 and os.path.exists('stdout') and not output_path:
        data['stdout'] = open('stdout').read()
    if int(os.environ.get('DEBUG', 0)) == 1 and os.path.exists('stderr') and not output_path:
        data['stderr'] = open('stderr').read()
    if int(os.environ.get('DEBUG', 0)) == 1 and output_path:
        data['diff']   = os.popen('diff -y stdout {}'.format(output_path)).read()
    json.dump(data, sys.stdout)
    sys.exit(status)

def run(argv):
    timeout = 10

    try:
        options, arguments = getopt.getopt(argv[1:], "t:v")
    except getopt.GetoptError as e:
        Logger.error(e)

    for option, value in options:
        if option == '-v':
            Logger.setLevel(logging.DEBUG)
        elif option == '-t':
            timeout = int(value)
        else:
            usage(1)

    if not arguments:
        usage(1)

    source      = arguments[0]
    input       = arguments[1]
    output      = arguments[2]
    executable  = os.path.splitext(os.path.basename(source))[0]

    try:
        language = get_language_from_source(source)
    except NotImplementedError:
        message  = 'Unable to determine language for {}'.format(source)
        return_result('Unknown', message, EXIT_FAILURE, COMPILER_ERROR)

    # Compile
    Logger.debug('Compiling {}...'.format(source))
    stdout  = open('stdout', 'w')
    stderr  = open('stderr', 'w')
    command = language.compile.format(source=source, executable=executable)
    try:
        subprocess.check_call(command, shell=True, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError:
        return_result(language.name, 'Compilation Error', EXIT_FAILURE, COMPILER_ERROR)

    # Execute
    Logger.debug('Executing {}...'.format(executable))
    command    = language.execute.format(source=source, executable=executable)
    stdout     = open('stdout', 'a')
    stdin      = open(input)
    start_time = time.time()
    toolong    = False

    try:
        process = subprocess.run(command.split(), stdin=stdin, stdout=stdout, stderr=stderr, timeout=timeout)
    except OSError:
        elapsed_time = time.time() - start_time
        return_result(language.name, 'Execution Error', EXIT_FAILURE, EXECUTION_ERROR, elapsed_time)
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return_result(language.name, 'Time Limit Exceeded', EXIT_FAILURE, TIMELIMIT_EXCEEDED, elapsed_time)
    finally:
        elapsed_time = time.time() - start_time

    if process.returncode != 0:
        return_result(language.name, 'Execution Error', process.returncode, EXECUTION_ERROR, elapsed_time)

    has_format_error = False
    for line0, line1 in itertools.zip_longest(open('stdout'), open(output)):
        if line0 is None or line1 is None:
            return_result(language.name, 'Wrong Answer', EXIT_FAILURE, WRONG_ANSWER, elapsed_time, output)

        if line0 != line1:
            line0 = ''.join(line0.strip().split()).lower()
            line1 = ''.join(line1.strip().split()).lower()
            if line0 == line1:
                has_format_error = True
            else:
                return_result(language.name, 'Wrong Answer', EXIT_FAILURE, WRONG_ANSWER, elapsed_time, output)

    if has_format_error:
        return_result(language.name, 'Output Format Error', EXIT_FAILURE, WRONG_FORMATTING, elapsed_time, output)
    else:
        return_result(language.name, 'Success', EXIT_SUCCESS, PROGRAM_SUCCESS, elapsed_time)

# Main Execution --------------------------------------------------------------

if __name__ == '__main__':
    # Set logging level
    logging.basicConfig(
        level   = logging.INFO,
        format  = '[%(asctime)s] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
    )

    # Run command
    run(sys.argv)

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
