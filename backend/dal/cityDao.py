from models import City

from dal.Database import Database

class CityDao:
    def __init__(self):
        self.database = Database()
    def getAllCity(self):
        con=self.database.con
        cursor=con.cursor()
        cursor.execute('SELECT * from city ;')
        data=cursor.fetchall()
        print(data)
        d=[]
        for line in data:
            d.append(City(line[1],int(line[0])))
        return d
    def AddCity(self,name):
            con = self.database.con
            cursor = con.cursor()
            print("***")
            try:
                cursor.execute(f'INSERT INTO city (name) VALUES ("{name}") ;')
                con.commit()  
                print("Insertion successful")  
            except Exception as e:
                print(f"An error occurred: {e}")
    def getCityById(self,id):
        con=self.database.con
        cursor=con.cursor()
        query = f'SELECT * FROM city where id = {id} ;'
        print(query)
        cursor.execute(query)
        l=cursor.fetchall()[0]
        print(l,"/////////")
        c= City(l[1],int(l[0]))
        return c
    