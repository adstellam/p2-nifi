from org.apache.nifi.controller import ControllerService
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from jarray import array
import json

class NiFiInputStreamCallback(InputStreamCallback):
    def __init__(self, conn, log):
        self.conn = conn
        self.log = log
    def process(self, inputStream):
        try: 
            str = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
            obj = json.loads(str)
            sql = 'INSERT INTO proto_plant (id, klass, confidence, odometer_meter) VALUES (?, ?, ?, ?);'
            pst = self.conn.prepareStatement(sql)
            pst.setInt(1, obj["id"])
            pst.setArray(2, self.conn.createArrayOf('INT', obj["klass"]))
            pst.setArray(3, self.conn.createArrayOf('REAL', obj["confidence"]))
            pst.setFloat(4, obj["odometer_meter"])
            pst.executeUpdate()
        except:
            self.log.error('SQL transaction failed and has been aborted.')
        
lookup = context.controllerServiceLookup
for cs in lookup.getControllerServiceIdentifiers(ControllerService):
    if lookup.getControllerServiceName(cs) == DatabaseConnectionPoolName.getValue():
        dbcpId = cs
if dbcpId:
    conn = lookup.getControllerService(dbcpId).getConnection()
    flowfile = session.get()
    if flowfile != None:
        try: 
            session.read(flowfile, NiFiInputStreamCallback(conn, log))
            session.transfer(flowfile, REL_SUCCESS)
        except:
            session.transfer(flowfile, REL_FAILURE)
        finally:
            conn.close()
        