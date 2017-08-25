Dredd
=====

Automated quiz and code grader.

Docker
------

Build:

    $ docker build -t pbui/dredd:20170814       < Dockerfile.submit     # GitLab CI
    $ docker build -t pbui/dredd-code:20170825  < Dockerfile.code       # Code run.py

Push:

    $ docker push pbui/dredd:20170814
    $ docker push pbui/dredd-code:20170825
