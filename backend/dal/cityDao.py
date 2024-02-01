from models import City
from Database import Database

class CityDao:
    def __init__(self):
        self.database = Database()
    def getAllCity(self):
        con=self.database.con
        cursor=con.cursor()
        cursor.execute('SELECT * city')
        d=[]
        for line in cursor.fetchall():
            d.append(City(line[1],int(line[0])))
        return d
    def AddCity(self,name):
            con = self.database.con
            cursor = con.cursor()
            try:
                cursor.execute('INSERT INTO city (name) VALUES (%s)',(name))
                con.commit()  
                print("Insertion successful")  
            except Exception as e:
                print(f"An error occurred: {e}")
    def getCityById(self,id):
        con=self.database.con
        cursor=con.cursor()
        l=cursor.execute(f'SELECT * FROM city where id = "{id}" ;') 
        c=City(l[1],int(l[0]))
        return c
    