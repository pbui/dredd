FROM	    ubuntu
MAINTAINER  Peter Bui <pbui@nd.edu>

RUN	    apt-get update -y
RUN	    apt-get install -y python-tornado python-requests python-yaml
RUN	    apt-get install -y gcc g++ python ruby perl default-jdk
