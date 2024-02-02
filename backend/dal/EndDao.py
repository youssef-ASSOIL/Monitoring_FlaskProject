
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
        
        disk=self.getDiskInfo(ip)
        ram=self.getRamInfo(ip)
        pr=self.getProcessorInfo(ip)
        if ram != []:
            print("1")
            infos=EndDeviceInfo()
            infos.diskSize = disk[0]
            infos.diskUsage = disk[1]
            infos.memorySize = ram[0]
            infos.memoryUsage = ram[1]
            infos.processorLoad = pr
            device.infos[""]= infos
            self.addEndDeviceInfo(device)
     
    

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
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        l="("
        for e in device.infos[""].processorLoad:
            l+= f" {e} , {device.id} , '{now}' ) ,("

        l=l[:-2]
        print(l)
        try:
            cursor.execute('INSERT INTO DeviceInfo (disksize, diskusage, memorysize, memoryusage, datetime, deviceid ) VALUES (%s, %s, %s, %s, %s,%s)',
                           (device.infos[""].diskSize,device.infos[""].diskUsage,device.infos[""].memorySize,device.infos[""].memoryUsage,now,device.id))
            con.commit()  

            cursor.execute(f'INSERT INTO Processor (processorload, deviceid,datetime) VALUES {l}')
            con.commit()  
            print("ok")
        except Exception as e:
            print(e)
        
        return device
        
    def getDeviceInfo(self,id):
        l={}
        con = self.database.con
        cursor = con.cursor()
        query=f"select * from EndDevice,Processor,DeviceInfo where Processor.deviceid = EndDevice.id and DeviceInfo.deviceid = EndDevice.id and Processor.datetime = DeviceInfo.datetime and EndDevice.id = {id}  ;"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        d=EndDevice(result[0][1],id,result[0][2],{})
        for line in result:
            if line[6] in d.infos:

                d.infos[line[6]].processorLoad.append(int(line[4]))
            else:
                deviceinfo = EndDeviceInfo()
                deviceinfo.diskSize = int(line[8])
                deviceinfo.diskUsage = int(line[9])
                deviceinfo.memorySize = int(line[10])
                deviceinfo.memoryUsage = int(line[11])
                deviceinfo.processorLoad.append(int(line[4]))
                d.infos[line[6]] = deviceinfo
        return d

        
    def getAllEndDevices(self):
        l=[]
        con = self.database.con
        cursor = con.cursor()
        query="select * from EndDevice ;"
        cursor.execute(query)
        result = cursor.fetchall()
        for line in result:
            l.append(EndDevice(line[1],int(line[0]),line[2],{}))
        return l
     
    
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

