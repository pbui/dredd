# Dredd

Automated quiz and code grader.

# Docker

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
