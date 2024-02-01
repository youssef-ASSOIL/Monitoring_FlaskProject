from dataclasses import dataclass
from dal.cityDao import CityDao
import requests
from datetime import datetime, timedelta


@dataclass
class CityService:
    def __init__(self):
        self.dao = CityDao() 
    def getAllCity(self):
        return self.dao.getAllCity()
    def AddCity(self,name):
        return self.dao.AddCity(name)
    

    def get_weather(self, lat, lon):
        seven_days_ago = datetime.now() - timedelta(days=7)
        formatted_date = seven_days_ago.strftime('%Y-%m-%d')

        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={formatted_date}&end_date={datetime.now().strftime("%Y-%m-%d")}&hourly=temperature_2m'
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()

            temperatures = data['hourly']['temperature_2m']
            return temperatures
        else:
            return "Failed to get weather data"
    
        
    def get_lat_lon(self, city_name):
        headers = {
            'User-Agent': 'YourAppName/1.0 (your-contact-info)'  
       }
        url = f'https://nominatim.openstreetmap.org/search?city={city_name}&format=json'
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()[0]  # Get the first result
            lat = data['lat']
            lon = data['lon']
            return lat, lon
        else:
            return None, None        

    def getCityById(self,id):
        name = self.dao.getCityById(id).name
        la,lo=self.get_lat_lon(name)
        c=self.get_weather(la,lo)
        return c