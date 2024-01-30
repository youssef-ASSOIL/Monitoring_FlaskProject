import mysql.connector as mysql
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
            con.commit()  # Commit the transaction
            print("Insertion successful")  # Confirm insertion
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            con.close()  # Close the connection