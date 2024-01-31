
from models import EndDevice,EndDeviceInfo
import subprocess
import json
import mysql.connector as mysql
from dal.Database import Database
from datetime import datetime

class EndDao:
    
    def __init__(self):
        self.database = Database()
    
    def hundle(self,device):
        ip=device.ipAdress
        print("rr")
        disk=self.getDiskInfo(ip)
        ram=self.getRamInfo(ip)
        pr=self.getProcessorInfo(ip)
        print(ip)
        print(disk,ram,pr)
    

    def addEndDevice(self,device):
        con = self.database.con
        cursor = con.cursor()
        
        try:
            cursor.execute('INSERT INTO EndDevice (name,ipadress) VALUES (%s, %s)',(device.name, device.ipAdress))
            con.commit() 
            device.id = cursor.lastrowid 
            return device
        except Exception as e:
            return None
        
    
    def addEndDeviceInfo(self,device):
        con = self.database.con
        cursor = con.cursor()

        l="("
        for e in device.infos.processorLoad:
            l+= f" {e} , {device.id} ) ,("

        l=l[:-2]
        try:
            cursor.execute('INSERT INTO DeviceInfo (disksize, diskusage, memorysize, memoryusage, datetime, deviceid ) VALUES (%s, %s, %s, %s, %s,%s)',
                           (device.infos.diskSize,device.infos.diskUsage,device.infos.memorySize,device.infos.memoryUsage,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),device.id))
            con.commit()  

            cursor.execute(f'INSERT INTO Processor (processorload, deviceid) VALUES {l}')
            con.commit()  
            return device
        except Exception as e:
            return None
        

        
    def getAllEndDevices(self):
        l=[]
        con = self.database.con
        cursor = con.cursor()
        query="select * from EndDevice ;"
        cursor.execute(query)
        result = cursor.fetchall()
        for line in result:
            l.append(EndDevice(line[1],int(line[0]),line[2],None))
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

    def getFrom(self,ip,oid):
        try:
            self.snmp_output=""
           
            tmp = subprocess.check_output(["snmpwalk", "-v2c", "-c", "public", ip ,oid ])
            tmp = tmp.decode("utf-8")
            self.snmp_output = tmp
            status=True
            return self.snmp_output
        except :
            return ""

    def getDiskInfo(self,ip):

        lines = self.getFrom(ip,"1.3.6.1.2.1.25.2.3").splitlines()
        res=[0,0]
        for l in lines:
            if "hrStorageSize" in l:
                res[0]+=int(l.split(" ")[3])
            elif "hrStorageUsed" in l:
                res[1]+=int(l.split(" ")[3])
        return res

    def getProcessorInfo(self,ip):
        lines = self.getFrom(ip,"1.3.6.1.2.1.25.3.3").splitlines()
        res=[]
        for l in lines:
            if "hrProcessorLoad" in l and len(l.split(":")) > 3:
                res.append(int(l.split(" ")[3]))

        return res

    def getRamInfo(self,ip):
        lines=self.getFrom(ip,"1.3.6.1.2.1.25.2.2.0")+self.getFrom(ip,"1.3.6.1.2.1.25.2.3.1.6.1")
        lines = lines.splitlines()
        res=[]
        for l in lines:
            if "hrMemorySize" in l and len(l.split(" ")) > 3:
                res.append(int(l.split(" ")[3]))
            elif "hrStorageUsed" in l and len(l.split(" ")) > 3:
                res.append(int(l.split(" ")[3]))

        return res

