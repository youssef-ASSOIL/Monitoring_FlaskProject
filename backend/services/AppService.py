
from dal.IotDao import IotDao
from dal.EndDao import EndDao
from time import sleep
import multiprocessing

class AppService():

    def __init__(self,iotdao,enddao) -> None:
        self.iotdao:IotDao = iotdao
        self.enddao:EndDao = enddao
        self.lock = multiprocessing.Lock()
    def hundle(self):
        
        while True:
            ds=self.iotdao.getAllDevices()
            ed=self.enddao.getAllEndDevices()
            with self.lock:
                for device in ds:
                    self.iotdao.hundle(device)



            with self.lock:
                for dv in ed:
                    self.enddao.hundle(dv)   

            sleep(10)

    def start(self):
        
        p = multiprocessing.Process(target=self.hundle)
        p.start()

    
         
    