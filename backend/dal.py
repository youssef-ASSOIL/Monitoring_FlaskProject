import mysql.connector as mysql
from models import IoT
import subprocess
import json
class Database:
    con = None
    @staticmethod
    def getConnection():
        if Database.con is None:
            try:
                Database.con = mysql.connect(
                    user='root',
                    password='1234',
                    database='flask_Monitoring',
                    host='db'
                )
            except Exception as e:
                print(f"Error connecting to the database: {e}")
        return Database.con
class IotDao:
    @staticmethod
    def getAllTemp():
        con=Database.getConnection()
        cursor=con.cursor()
        cursor.execute('SELECT * FROM iotdevices')
        return cursor.fetchall()
    
    @staticmethod
    def getAllDevices():
        l=[]
        try:
            con=Database.getConnection()
            cursor=con.cursor()
            cursor.execute('SELECT * FROM iot_devices')
            for line in cursor.fetchall():
                l.append(IoT(line[3],line[0],None,None,float(line[1]),float(line[2])))

        except:
            pass
        
        return l
    
    @staticmethod
    def hundle(device):
        command = ["mosquitto_sub", "-h", "test.mosquitto.org", "-t", device.name, "-C", "1"]
        try:   
            result = subprocess.run(command, text=True, capture_output=True, timeout=10)

            if result.returncode == 0 and result.stdout:
                        
                message_json = result.stdout.strip()
                message_data = json.loads(message_json)  
                temperature = float(message_data.get('temperature'))
                datetime = message_data.get('time')

            if temperature is not None and datetime is not None:
                IotDao.insertIntoTemperature(temperature,device.mac,datetime)
        except Exception as e:
            pass
    @staticmethod
    def getAllTempReadings():
        con=Database.getConnection()
        cursor=con.cursor()
        cursor.execute('SELECT * FROM temperature_readings')
        return cursor.fetchall()
    
    @staticmethod
    def insertIntoTemperature(temperature, mac, datetime):
        con = Database.getConnection()
        cursor = con.cursor()
        try:
            print(f"Inserting: Temperature: {temperature}, MAC: {mac}, Datetime: {datetime}")  # Debug print
            cursor.execute('INSERT INTO temperature_readings (temperature, mac, datetime) VALUES (%s, %s, %s)',
                           (temperature, mac, datetime))
            con.commit()  
            print("Insertion successful")  
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            con.close()  