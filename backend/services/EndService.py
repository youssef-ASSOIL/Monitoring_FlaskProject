from dataclasses import dataclass
import subprocess

from dal import EndDao


@dataclass
class SnmpService:
    snmp_output:str=""
    status:bool=False
    dao:EndDao=EndDao()
    
    def addEndDevice(self,device) :
        self.dao.addEndDevice(device)
        if self.getFrom(device.ipAdress) != "" :
            return True
        return False
        
    
    def getFrom(self,ip):
        try:
            # Run snmpwalk command and capture the output
            snmp_output = subprocess.check_output(["snmpwalk", "-v2c", "-c", "public", ip , "1.3.6.1.2.1.25.3.3","1.3.6.1.2.1.25.2.3","1.3.6.1.2.1.25.2.2.0","1.3.6.1.2.1.25.2.3.1.6.1"])
            snmp_output = snmp_output.decode("utf-8")
            self.snmp_output = snmp_output
            status=True
            return snmp_output
        except :
            return ""

    def getDiskInfo(self):

        lines = self.snmp_output.splitlines()
        res=[0,0]
        for l in lines:
            if "hrStorageSize" in l:
                res[0]+=int(l.split(" ")[3])
            elif "hrStorageUsed" in l:
                res[1]+=int(l.split(" ")[3])
        return res

    def getProcessorInfo(self):
        lines = self.snmp_output.splitlines()
        res=[]
        for l in lines:
            if "hrProcessorLoad" in l and len(l.split(":")) > 3:
                res.append(int(l.split(" ")[3]))

        return res

    def getRamInfo(self):
        lines = self.snmp_output.splitlines()
        res=[]
        for l in lines:
            if "hrMemorySize" in l and len(l.split(" ")) > 3:
                res.append(int(l.split(" ")[3]))
            elif "hrStorageUsed" in l and len(l.split(" ")) > 3:
                res.append(int(l.split(" ")[3]))

        return res
