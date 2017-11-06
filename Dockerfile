FROM ubuntu:14.04

RUN echo "nameserver 2a02:6b8:0:3400::1023" > /etc/resolv.conf
RUN apt-get update
RUN apt-get -y install  python-virtualenv python-dev build-essential python-all-dev git

RUN mkdir /opt/docker-worker
RUN virtualenv /opt/docker-worker/venv
RUN /opt/docker-worker/venv/bin/pip install git+https://github.com/andreiSaw/pydisneyland
RUN /opt/docker-worker/venv/bin/pip install git+https://github.com/sashabaranov/easywebdav
RUN /opt/docker-worker/venv/bin/pip install git+https://github.com/andreiSaw/hep-data-backends
RUN /opt/docker-worker/venv/bin/pip install git+https://github.com/andreiSaw/docker-worker

ADD configs /opt/docker-worker/configs
ADD docker-worker /opt/docker-worker/dockerworker
