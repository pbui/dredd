FROM	    ubuntu
MAINTAINER  Peter Bui <pbui@nd.edu>

RUN	    apt update -y

# Run-time dependencies
RUN	    apt install -y python-tornado python-requests python-yaml wget

# Language Support: C, C++, Python, Ruby, Perl, Java
RUN	    apt install -y gcc g++ python ruby perl default-jdk

# Language Support: Swift
RUN	    apt install -y clang libicu-dev libpython2.7; \
	    mkdir -p /opt; \
	    cd /opt; \
	    wget https://swift.org/builds/swift-3.1.1-release/ubuntu1604/swift-3.1.1-RELEASE/swift-3.1.1-RELEASE-ubuntu16.04.tar.gz; \
	    tar xzvf swift-3.1.1-RELEASE-ubuntu16.04.tar.gz; \
	    mv swift-3.1.1-RELEASE-ubuntu16.04 swift-3.1.1; \
	    mv swift-3.1.1/usr/* swift-3.1.1/; \
	    rm -fr swift-3.1.1/usr; \
	    rm swift-3.1.1-RELEASE-ubuntu16.04.tar.gz

