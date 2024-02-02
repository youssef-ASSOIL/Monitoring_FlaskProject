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
                    host='35.203.112.244'
                )
        except:
            self.status = False