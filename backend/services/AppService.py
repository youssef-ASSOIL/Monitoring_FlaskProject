
from dal import IotDao
from time import sleep
import multiprocessing

class AppService():

    def hundle(self):
        
        while True:
            ds=IotDao.getAllDevices()
            print("aa")
            for device in ds:
                
                IotDao.hundle(device)
                
            print("qqq")
            sleep(6)

    def start(self):
        
        p = multiprocessing.Process(target=self.hundle)
        p.start()

    
         
    