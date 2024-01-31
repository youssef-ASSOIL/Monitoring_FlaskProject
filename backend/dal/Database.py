import mysql.connector as mysql

class Database:
    
    def __init__(self):
        self.status = True
        self.con = None
        try:
            self.con = mysql.connect(
                    user='admin',
                    password='Admin1234',
                    database='flask_Monitoring',
                    host='34.95.30.36'
                )
        except Exception as e:
            self.status = False