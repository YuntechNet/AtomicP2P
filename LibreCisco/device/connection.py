import time
import telnetlib
from paramiko import SSHClient, AutoAddPolicy
from pysnmp.entity import config
from pysnmp.hlapi.asyncore import *


class SNMPv3Connection(object):

    def __init__(self, authentication):
        userName = authentication['account']
        host = authentication['host']
        authProtocol = self.get_protocol(
                            auth_or_priv='AUTH',
                            protocol_str=authentication['auth_protocol'])
        privProtocol = self.get_protocol(
                            auth_or_priv='PRIV',
                            protocol_str=authentication['priv_protocol'])
        authKey = authentication['auth_password']
        privKey = authentication['priv_password']
        assert type(host) == tuple
        self._snmpEngine = SnmpEngine()
        self._userData = UsmUserData(userName=userName, authKey=authKey,
                                     authProtocol=authProtocol,
                                     privKey=privKey,
                                     privProtocol=privProtocol)
        self._udpTransportTarget = UdpTransportTarget(host)
        self._output = []

    def get_protocol(self, auth_or_priv, protocol_str):
        auth_or_priv = auth_or_priv.upper()
        protocol_str = protocol_str.upper() if protocol_str else None
        auth_protocols = {
            'MD5': config.usmHMACMD5AuthProtocol,
            'SHA': config.usmHMACSHAAuthProtocol,
            'SHA224': config.usmHMAC128SHA224AuthProtocol,
            'SHA256': config.usmHMAC192SHA256AuthProtocol,
            'SHA384': config.usmHMAC256SHA384AuthProtocol,
            'SHA512': config.usmHMAC384SHA512AuthProtocol
        }
        priv_protocols = {
            'DES': config.usmDESPrivProtocol,
            '3DES': config.usm3DESEDEPrivProtocol,
            'AES': config.usmAesCfb128Protocol,
        }
        if auth_or_priv == 'AUTH':
            return auth_protocols[protocol_str] \
                   if protocol_str in auth_protocols \
                   else config.usmNoAuthProtocol
        else:
            return priv_protocols[protocol_str] \
                   if protocol_str in priv_protocols \
                   else config.usmNoPrivProtocol

    def response(self, snmpEngine, sendRequestHandler, errorIndication,
                 errorStatus, errorIndex, varBindTable, cbCtx):
        if errorIndication:
            self._output.append(errorIndication)
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
        if type(oid) != list:
            oid = [oid]
        self._output.clear()
        for each in oid:
            assert type(each) == ObjectType
            getCmd(self._snmpEngine, self._userData, self._udpTransportTarget,
                   ContextData(), each, cbFun=self.response)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def bulk(self, oid_with_NR):
        if type(oid_with_NR) != list:
            oid_with_NR = [oid_with_NR]
        self._output.clear()
        for each in oid_with_NR:
            oid = each[0]
            NR = each[1]
            assert type(oid) == ObjectType
            assert type(NR) == tuple
            bulkCmd(self._snmpEngine, self._userData, self._udpTransportTarget,
                    ContextData(), NR[0], NR[1], oid, cbFun=self.response)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def output(self):
        return self._output

    def get_output(self, oid):
        self.get(oid=oid)
        return self._output

    def bulk_output(self, oid_with_NR):
        self.bulk(oid_with_NR=oid_with_NR)
        return self._output


class TelnetConnection(object):

    def __init__(self, authentication, debug_level=0):
        self.host = authentication['host']
        self.username = authentication['account']
        self.password = authentication['password']
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

    def __init__(self, authentication, timeout=60):
        self.host = (authentication['host'][0], int(authentication['host'][1]))
        self.username = authentication['account']
        self.password = authentication['password']
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
