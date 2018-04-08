FROM ubuntu:16.04

RUN apt-get update && apt-get install -y software-properties-common apt-utils wget \
                                         libjpeg-dev git locales curl

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-add-repository ppa:jonathonf/python-3.6
RUN apt-get update && apt-get install -y python3.6 python3.6-dev python3.6-venv python3-pip

RUN ln -s /usr/bin/python3.6 /usr/bin/python
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6

COPY requirements.txt /var/www/app/requirements.txt
WORKDIR /var/www/app

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

ADD . /var/www/app

ENV FLASK_APP run.py

ENTRYPOINT ["./entrypoint.sh"]
