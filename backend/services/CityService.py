from dataclasses import dataclass
from dal.cityDao import CityDao
import requests
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_absolute_error

@dataclass
class CityService:
    def __init__(self):
        self.dao = CityDao() 
    def getAllCity(self):
        return self.dao.getAllCity()

    def AddCity(self,name):
        self.dao.AddCity(name)
    

    def get_weather(self, lat, lon):
        seven_days_ago = datetime.now() - timedelta(days=7)
        formatted_date = seven_days_ago.strftime('%Y-%m-%d')

        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={formatted_date}&end_date={datetime.now().strftime("%Y-%m-%d")}&hourly=temperature_2m'
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()

            temperatures = data['hourly']['temperature_2m']
            timestamps = data['hourly']['time']  

            dates = [datetime.fromisoformat(ts).strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

            return [dates, temperatures]
        else:
            return []
    
        
    def get_lat_lon(self, city_name):
        headers = {
            'User-Agent': 'YourAppName/1.0 (your-contact-info)'  
       }
        url = f'https://nominatim.openstreetmap.org/search?city={city_name}&format=json'
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and len(response.json()) > 0:
            data = response.json()[0] 
            lat = data['lat']
            lon = data['lon']
            return lat, lon
        else:
            return None, None        

    def getCityById(self,id):
        name = self.dao.getCityById(id).name

        print("+++",name)
        la,lo=self.get_lat_lon(name)
        print("....",la,lo)
        c=self.get_weather(la,lo)
        print("----",c)
        

        return c


    def predict_future_temperatures(self,historical_dates, historical_temperatures, num_future_days):
        dates = np.array(historical_dates).reshape(-1, 1)
        temperatures = np.array(historical_temperatures).astype(float).reshape(-1, 1)


        X_train, X_test, y_train, y_test = train_test_split(dates, temperatures, test_size=0.2, random_state=0)

        model = LinearRegression()
        model.fit(X_train, y_train)

        last_date = max(historical_dates)
        future_dates = np.array(range(last_date + 1, last_date + 1 + num_future_days)).reshape(-1, 1)
        predicted_temperatures = model.predict(future_dates)

        future_dates_list = future_dates.flatten().tolist()
        predicted_temperatures_list = predicted_temperatures.flatten().tolist()

        return [future_dates_list, predicted_temperatures_list]