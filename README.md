# Dredd

Automated quiz and code grader.

# Running Dredd

To run `dredd`, you can do the following:

    $ python3 dredd --logging=debug
    
This will start the dredd server with debug level logging.

# Docker Containers

Internally, `dredd` uses docker to execute submitted code in an isolated
container.  The precise docker image is defined in the `scripts/sandbox.sh`
script (ie. `IMAGE`).

Provided in this repository are two `Dockerfiles`:

- `Dockerfile.submit`: This provides an example of a simple docker container
  that can be used to submit quizzes and code to `dredd`.
    
- `Dockerfile.code`: This provides an example of a simple docker container that
  will be used to execute code in isolation.  As such, it should contain the
  interpreters and compilers required by `dredd` and the `scripts/run.py`
  script.

Build:

    $ docker build -t pbui/dredd:20170814      - < Dockerfile.submit     # GitLab CI
    $ docker build -t pbui/dredd-code:20170825 - < Dockerfile.code       # Code run.py

Push:

    $ docker push pbui/dredd:20170814
    $ docker push pbui/dredd-code:20170825
    
# Programming Languages

To add support for a programming language, you must do the following:

1. Update `Dockerfile.code` to include the interpreter or compiler.

2. Update `scripts/run.py` to include a rule for the programming language. For
   instance, to support `C` and `Python`, you need to specify the following:

    ```
    Language('C',                                       # Language
        'gcc -std=gnu99 -o {executable} {source} -lm',  # Compilation
        './{executable}',                               # Execution
        ('.c',)                                         # Extension
    ),
    Language('Python',                                  # Language
        '',                                             # Compilation
        'python3 {source}',                             # Execution
        ('.py',)                                        # Extension
    ```
    
3. Update `tests/test_code_echo.sh` to include a simple **echo** test for that
   language (ie. the program reads in the input and echos it back).
