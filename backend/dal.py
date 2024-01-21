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
