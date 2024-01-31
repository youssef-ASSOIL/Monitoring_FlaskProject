from dal.IotDao import IotDao 

class IotService():
    
    def __init__(self):
        self.dao = IotDao()

    def getAllTemp(self):
        return self.dao.getAllTemp()
   
    def getAllTempReadings(self):
        return self.dao.getAllTempReadings()
    
