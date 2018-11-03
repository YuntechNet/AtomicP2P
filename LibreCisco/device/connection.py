import time
import telnetlib
from paramiko import SSHClient, AutoAddPolicy
from pysnmp.entity import config
from pysnmp.hlapi.asyncore import *


class SNMPv3Connection(object):

    def __init__(self, userName, authKey, host, authProtocol=None,
                 privProtocol=None):
        assert type(host) == tuple
        self._snmpEngine = SnmpEngine()
        self._userData = UsmUserData(userName=userName, authKey=authKey,
                                     authProtocol=authProtocol)
        self._udpTransportTarget = UdpTransportTarget(host)
        self._output = []

    def response(self, snmpEngine, sendRequestHandler, errorIndication,
                 errorStatus, errorIndex, varBindTable, cbCtx):
        self._output.clear()
        if errorIndication:
            self._output.append(errirIndication)
            return
        elif errorStatus:
            self._output.append(
                '{} = {}'.format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex) - 1][0]
                    or '?'))
        else:
            for varBindRow in varBindTable:
                if type(varBindRow) != list:
                    varBindRow = [varBindRow]
                for varBind in varBindRow:
                    self._output.append(
                        ' = '.join([x.prettyPrint() for x in varBind]))

    def get(self, oid):
        assert type(oid) == ObjectType
        getCmd(self._snmpEngine, self._userData, self._udpTransportTarget,
               ContextData(), oid, cbFun=self.response)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def bulk(self, oid, NR):
        assert type(oid) == ObjectType
        bulkCmd(self._snmpEngine, self._userData, self._udpTransportTarget,
                ContextData(), NR[0], NR[1], oid, cbFun=self.response)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def output(self):
        return self._output


class TelnetConnection(object):

    def __init__(self, host, username, password, debug_level=0):
        self.host = host
        self.username = username
        self.password = password
        self.debug_level = debug_level

    def login(self, debug_level=None):
        debug_level = debug_level if debug_level else self.debug_level
        self.client = telnetlib.Telnet(self.host)
        self.client.set_debuglevel(debug_level)
        if self.username:
            self.client.read_until(bytes('login: ', encoding='utf-8'))
            self.client.write(bytes(self.username + '\n', encoding='utf-8'))
        self.client.read_until(bytes('Password ', encoding='utf-8'))
        self.client.write(bytes(self.password + '\n', encoding='utf-8'))
        return self

    def sendCommand(self, command, wrap=True):
        self.client.write(bytes(command + ('\n' if wrap else ''),
                                encoding='utf-8'))

    def logout(self):
        if self.client:
            self.client.close()

    def is_active(self):
        try:
            if self.client.sock:
                self.client.sock.send(telnetlib.IAC + telnetlib.NOP)
                self.client.sock.send(telnetlib.IAC + telnetlib.NOP)
                self.client.sock.send(telnetlib.IAC + telnetlib.NOP)
                return True
        except Exception as e:
            pass
        return False


class SSHConnection(object):

    def __init__(self, host, username, password, timeout=60):
        self.host = (host[0], int(host[1]))
        self.username = username
        self.password = password
        self.timeout = timeout

        self.client, self.shell, self.output = None, None, None

    def login(self, timeout=None):
        self.timeout = timeout if timeout is not None else self.timeout
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=self.host[0], port=self.host[1],
                            username=self.username, password=self.password,
                            timeout=self.timeout, look_for_keys=False,
                            allow_agent=False)
        self.shell = self.client.invoke_shell()
        self.output = self.shell.recv(65535)
        return self

    def logout(self):
        if self.client:
            self.client.close()

    def send_command(self, command, wrap=True, time_sleep=0.5, short=True):
        self.shell.send(str(command) + ('\n' if wrap else ''))
        time.sleep(time_sleep)
        output = self.shell.recv(65535).decode('utf-8')
        while ('#' not in output and '>' not in output):
            if ' --More-- ' in output:
                output = output.replace(' --More-- ', '') + \
                         self.send_command(command='q' if short else ' ',
                                           wrap=False, time_sleep=time_sleep,
                                           short=short)
            elif self.is_active():
                output += self.shell.recv(65535).decode('utf-8')
            else:
                break
        self.output = output
        return self.output

    def send_commands(self, commands, wrap=True, time_sleep=0.5, short=True):
        if type(commands) == list:
            output = ''
            for each in commands:
                output += self.send_command(
                                command=each, wrap=wrap, time_sleep=time_sleep,
                                short=short)
            return output
        else:
            return self.send_command(command=commands, wrap=wrap,
                                     time_sleep=time_sleep)

    def is_active(self):
        if self.client and self.client.get_transport():
            return self.client.get_transport().is_active()
        return False
