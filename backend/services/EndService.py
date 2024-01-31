from dataclasses import dataclass
import subprocess

from dal.EndDao import EndDao


@dataclass
class EndService:
    snmp_output:str=""
    status:bool=False
    dao:EndDao=EndDao()
    
    def addEndDevice(self,device) :
        
        result = self.dao.getFrom(device.ipAdress)
        if result != "" :
            d=self.dao.addEndDevice(device)
            if d == None:
                return False
            
            

            return True
        return False
    

    def getEndDevices(self):
        return self.dao.getAllEndDevices()
        
    
    