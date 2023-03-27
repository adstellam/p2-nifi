from org.apache.nifi.controller import ControllerService
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
import json

class NiFiInputStreamCallback(InputStreamCallback):
    def __init__(self, session, log, REL_SUCCESS, REL_FAILURE, conn, flowfile):
        self.session = session
        self.log = log
        self.REL_SUCCESS = REL_SUCCESS
        self.REL_FAILURE = REL_FAILURE
        self.conn = conn
        self.flowfile = flowfile
    def process(self, inputStream):
        try:
            str = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
            obj = json.loads(str)
            sql = 'INSERT INTO proto_plant (id, klass, confidence, odometer_meter) VALUES (?, ?, ?, ?);'
            pst = self.conn.prepareStatement(sql)
            pst.setInt(1, 3333)
            pst.setArray(2, null)
            pst.setArray(3, null)
            pst.setFloat(4, 44.44)
            pst.executeUpdate()
            self.session.transfer(self.flowfile, self.REL_SUCCESS)
        except:
            self.log.error('SQL transaction failed and has been rolled back.')
            self.session.transfer(self.flowfile, self.REL_FAILURE)
        finally:
            self.conn.close()
        
lookup = context.controllerServiceLookup
for cs in lookup.getControllerServiceIdentifiers(ControllerService):
    if lookup.getControllerServiceName(cs) == DatabaseConnectionPoolName.getValue():
        dbcpId = cs
if dbcpId:
    conn = lookup.getControllerService(dbcpId).getConnection()

flowfile = session.get()
if flowfile != None:
    session.read(flowfile, NiFiInputStreamCallback(session, log, REL_SUCCESS, REL_FAILURE, conn, flowfile))
