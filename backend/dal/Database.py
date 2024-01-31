import mysql.connector as mysql

class Database:
    
    def __init__(self):
        self.status = True
        self.con = None
        try:
            self.con = mysql.connect(
                    user='root',
                    password='',
                    database='flask_Monitoring',
                    host='localhost'
                )
        except Exception as e:
            self.status = False