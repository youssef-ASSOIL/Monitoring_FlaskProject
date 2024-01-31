
from models import EndDevice,EndDeviceInfo
import subprocess
import json
import mysql.connector as mysql
from Database import Database


class IotDao:
    
    def __init__(self):
        self.database = Database()
    

    def addEndDevice(self,device):
        con = self.database.con
        cursor = con.cursor()
        
        try:
            cursor.execute('INSERT INTO EndDevice (name,ipadress) VALUES (%s, %s)',(device.name, device.ipAdress))
            con.commit()  
            return device
        except Exception as e:
            return None
        

        
    def getAllEndDevices(self):
        l=[]
        con = self.database.con
        cursor = con.cursor()
        query="select * from EndDevice,DeviceInfo where EndDevice.id = DeviceInfo.deviceid ;"
        cursor.execute(query)
        result = cursor.fetchall()
       
        print(result)
        return l
        '''
        for line in result:
                id=int(line[0])
                i=EndDeviceInfo(int(line[]),int(line[]),int(line[]),int(line[]),getEndDeviceProcessors(id))
                l.append(EndDevice(id,line[],i))
        return l
        '''
    
    def getEndDeviceProcessors(self,id):
        r=[]
        query="select * from Processor where deviceid = id ;"
        con = self.database.con
        cursor = con.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
       

        for line in result:
            r.append(int(line[1]))

        return r

