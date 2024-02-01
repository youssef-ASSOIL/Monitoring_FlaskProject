from dal.IotDao import IotDao 

class IotService():
    
    def __init__(self):
        self.dao = IotDao()

    def getAllTemp(self):
        return self.dao.getAllTemp()
   
    def getAllTempReadings(self,mac):
        return self.dao.getAllTempReadings(mac)
    
    def addIotDevice(self,d):
        self.dao.addIotDevice(d)

    def getAllDevices(self):
        return self.dao.getAllDevices()