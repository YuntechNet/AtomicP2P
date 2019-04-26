FROM ubuntu:16.04

MAINTAINER clooooode<jackey8616@gmail.com>

EXPOSE 22 23

COPY ./ubuntu.start.sh start.sh

RUN apt-get update
RUN apt-get install openssh-server -y
RUN apt-get install xinetd telnetd -y

CMD sh ./start.sh
