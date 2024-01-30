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

   