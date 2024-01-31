import mysql.connector as mysql


try:
    con = mysql.connect(
            user='admin',
            password='Admin1234',
            database='flask_Monitoring',
            host='34.95.30.36'
                )
    print("ok")
except Exception as e:
    print(e)