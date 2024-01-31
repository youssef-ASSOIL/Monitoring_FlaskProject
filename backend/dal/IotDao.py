
from models import IoT
import subprocess
import json
import mysql.connector as mysql
from dal.Database import Database



class IotDao:
    
    def __init__(self):
        self.database = Database()
    
    
    def getAllTemp(self):
        con=self.database.con
        cursor=con.cursor()
        cursor.execute('SELECT * FROM iotdevices')
        return cursor.fetchall()
    
   
    def getAllDevices(self):
        l=[]
        try:
            con=self.database.con
            cursor=con.cursor()
            cursor.execute('SELECT * FROM iot_devices')
            for line in cursor.fetchall():
                l.append(IoT(line[3],line[0],None,None,float(line[1]),float(line[2])))

        except:
            pass
        
        return l
    
    
    def hundle(self,device):
        command = ["mosquitto_sub", "-h", "test.mosquitto.org", "-t", device.name, "-C", "1"]
        try:   
            result = subprocess.run(command, text=True, capture_output=True, timeout=10)

            if result.returncode == 0 and result.stdout:
                        
                message_json = result.stdout.strip()
                message_data = json.loads(message_json)  
                temperature = float(message_data.get('temperature'))
                datetime = message_data.get('time')

            if temperature is not None and datetime is not None:
                self.insertIntoTemperature(temperature,device.mac,datetime)
        except Exception as e:
            pass
    

    def getAllTempReadings(self):
        con=self.database.con
        cursor=con.cursor()
        cursor.execute('SELECT * FROM temperature_readings')
        return cursor.fetchall()
    
   
    def insertIntoTemperature(self,temperature, mac, datetime):
        con = self.database.con
        cursor = con.cursor()
        try:
            print(f"Inserting: Temperature: {temperature}, MAC: {mac}, Datetime: {datetime}")  # Debug print
            cursor.execute('INSERT INTO temperature_readings (temperature, mac, datetime) VALUES (%s, %s, %s)',
                           (temperature, mac, datetime))
            con.commit()  
            print("Insertion successful")  
        except Exception as e:
            print(f"An error occurred: {e}")
       


