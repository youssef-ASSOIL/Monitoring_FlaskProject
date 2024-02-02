from dataclasses import dataclass
import subprocess

from dal.EndDao import EndDao


@dataclass
class EndService:
    snmp_output:str=""
    status:bool=False
    dao:EndDao=EndDao()
    
    def addEndDevice(self,device) :
        print("*************")
        result = self.dao.getFrom(device.ipAdress,"1.3.6.1.2.1.25.2.3")
        print("----------------",result)
        if result != "" :
            d=self.dao.addEndDevice(device)
            if d == None:
                return False
            
            

            return True
        return False
    

    def getEndDevices(self):
        return self.dao.getAllEndDevices()
    
    def getDeviceInfo(self,id):
        return self.dao.getDeviceInfo(id)
        
    
    