FROM ubuntu:16.04

EXPOSE 22 25

RUN apt-get update
RUN apt-get install openssh-server -y
RUN apt-get install xinetd telnetd -y

# Telnet
RUN sed -i 's/# log_type = SYSLOG daemon info/instances = 60\nlog_type = SYSLOG authpriv\nlog_on_success = HOST PID\nlog_on_failure = HOST\ncps = 25 30/' /etc/xinetd.conf
RUN sed -i 's/auth \[success=ok/# auth \[success=ok/' /etc/pam.d/login
RUN echo 'telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd' > /etc/inetd.conf

# SSH
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN echo "export VISIBLE=now" >> /etc/profile

RUN service ssh start
RUN service xinetd start

ENTRYPOINT ["/bin/bash"]
