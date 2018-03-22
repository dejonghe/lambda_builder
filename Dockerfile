from amazonlinux:latest

# Update yum to ensure we have the latest 
RUN yum update

# Setup app dir
RUN mkdir /app

# Install the main languages (2.7 is already setup)
RUN yum install -y python27-pip python36 python36-pip golang java-1.8.0-openjdk

# Setup Go Vars
ENV GOPATH=/root/gocode/
ENV GOBIN=/root/gocode/bin/
ENV PATH=$PATH:$GOBIN


# Ready the build dir
RUN mkdir /build
VOLUME /build

# Read app
COPY ./ /var/app/
WORKDIR /var/app
RUN python3.6 setup.py sdist && \
    pip-3.6 install dist/lambda_builder-0.0.0.tar.gz


WORKDIR /build 



CMD lambda_builder
