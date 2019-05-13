#!/bin/bash

# Telnet
sed -i 's/# log_type = SYSLOG daemon info/instances = 60\nlog_type = SYSLOG authpriv\nlog_on_success = HOST PID\nlog_on_failure = HOST\ncps = 25 30/' /etc/xinetd.conf
sed -i 's/auth \[success=ok/# auth \[success=ok/' /etc/pam.d/login
echo 'telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd' > /etc/inetd.conf

# SSH
echo 'root:toor' | chpasswd
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
echo "export VISIBLE=now" >> /etc/profile

service xinetd start
service ssh start

while sleep 60; do
  service xinetd status | grep 'is running'
  service ssh status | grep 'is running'
done
