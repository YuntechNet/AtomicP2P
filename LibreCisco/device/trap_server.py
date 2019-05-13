from pysnmp.entity import config
from pysnmp.hlapi.asyncore import SnmpEngine
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

from LibreCisco.utils.manager import ThreadManager


class TrapServer(ThreadManager):

    def __init__(self):
        super(TrapServer, self).__init__()
        self._pdu_count = 1
        self._snmpEngine = SnmpEngine()
        config.addTransport(
            self._snmpEngine, udp.domainName,
            udp.UdpTransport().openServerMode(('0.0.0.0', 162))
        )
        self.addUser(authentication={
            'userName': 'TestUser',
            'auth_protocol': config.usmHMACSHAAuthProtocol,
            'auth_key': 'TestAuth',
            'priv_protocol': config.usmDESPrivProtocol, 'priv_key': 'TestAuth',
            'engineId': '800000d30300000e112245'
        })
        ntfrcv.NotificationReceiver(self._snmpEngine, self.cbFun)

    def run(self):
        self._snmpEngine.transportDispatcher.jobStarted(1)
        self._snmpEngine.transportDispatcher.runDispatcher()

    def stop(self):
        self._snmpEngine.transportDispatcher.jobFinished(1)

    def addUser(self, authentication):
        config.addV3User(
            snmpEngine=self._snmpEngine, userName=authentication['userName'],
            authProtocol=authentication['auth_protocol'],
            authKey=authentication['auth_key'],
            privProtocol=authentication['priv_protocol'],
            privKey=authentication['priv_key'],
            securityEngineId=v2c.OctetString(
                hexValue=authentication['engineId'])
        )
    
    def cbFun(self, stateReference, contextEngineId, contextName, varBinds,
              cbCtx):
        print("####################### NEW Notification(PDU_COUNT: {}) ######"\
               "#################".format(self._pdu_count))
        execContext = self._snmpEngine.observer.getExecutionContext(
            "rfc3412.receiveMessage:request"
        )
        print("#Notification from " + 
            ("@".join([str(x) for x in execContext['transportAddress']])))
        print("#ContextEngineId: {}".format(contextEngineId.prettyPrint()))
        print("#ContextName: {}".format(contextName.prettyPrint()))
        print("#SNMPVER {}".format(execContext['securityModel']))
        print("#SecurityName {}".format(execContext['securityName']))
        for oid, val in varBinds:
            print(oid, val)
        self._pdu_count +=1
