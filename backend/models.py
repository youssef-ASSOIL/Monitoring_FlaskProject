from dataclasses import dataclass


@dataclass
class Device:
    name:str

@dataclass
class IoT(Device):
    mac:str
    temp:float
    datetime:str
    latitude:float
    longitude:float

   
@dataclass
class EndDeviceInfo():
    diskSize:int
    diskUsage:int
    memorySize:int
    memoryUsage:int
    processorLoad:list[int]

    def __init__(self):
        self.processorLoad = []



@dataclass
class EndDevice(Device):
    id:int
    ipAdress:str
    infos:dict


