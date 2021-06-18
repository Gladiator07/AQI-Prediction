from datetime import datetime
from geopy.geocoders import Nominatim
import requests
import pandas as pd
from datetime import date, timedelta

ts = int("1284101485")

# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))


def lat_lng(city):

    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(city, addressdetails=True)
    latitude, longitude = location.latitude, location.longitude


    return latitude, longitude
def fetch_future_air_data(city):
    latitude, longitude = lat_lng(city)
    if latitude and longitude:
        api_key = "9d7cde1f6d07ec55650544be1631307e"

        URL = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}&appid={api_key}"

        response = requests.get(URL)

        # current_aiq = 
        
        air_data = response.json()
        rows = []
        for i in range((len(air_data["list"]))):
            
            air_data["list"][i]["dt"] = datetime.utcfromtimestamp(air_data["list"][i]["dt"]).strftime('%Y-%m-%d %H')
            air_contents = air_data["list"][i]["components"]
            
            date_1 = air_data["list"][i]["dt"].split(' ')[0]
            time = air_data["list"][i]["dt"].split(' ')[1]
            AQI = air_data["list"][i]["main"]["aqi"]
            co = air_contents["co"]
            no = air_contents["no"]
            no2 = air_contents["no2"]
            o3 = air_contents["o3"]
            so2 = air_contents["so2"]
            pm2_5 = air_contents["pm2_5"]
            pm10 = air_contents["pm10"]
            nh3 = air_contents["nh3"]
            
            rows.append([date_1,time,AQI,co,no,no2,o3,so2,pm2_5,pm10,nh3])
        df = pd.DataFrame(rows, columns=["date","time","AQI","co","no","no2","o3","so2","pm2_5","pm10","nh3"])
        df.to_csv("test_1.csv")
        today = date.today()
        today_disp = str(date.today())
        first_day = str(today + timedelta(days=1))
        second_day = str(today + timedelta(days=2))
        third_day = str(today + timedelta(days=3))
        fourth_day = str(today + timedelta(days=4))
        fifth_day = str(today + timedelta(days=5))

        data_today = df[df['date'] == today_disp].reset_index(drop=True)
        data_first = df[df['date'] == first_day].reset_index(drop=True)
        data_second = df[df['date'] == second_day].reset_index(drop=True)
        data_third = df[df['date'] == third_day].reset_index(drop=True)
        data_fourth = df[df['date'] == fourth_day].reset_index(drop=True)
        data_fifth = df[df['date'] == fifth_day].reset_index(drop=True)

        pre_first_day = str(today - timedelta(days=1))
        pre_second_day = str(today-  timedelta(days=2))
        pre_third_day = str(today - timedelta(days=3))
        pre_fourth_day = str(today-  timedelta(days=4))
        pre_fifth_day = str(today - timedelta(days=5))

        pre_data_first = df[df['date'] == pre_first_day].reset_index(drop=True)
        pre_data_second = df[df['date'] ==pre_second_day].reset_index(drop=True)
        pre_data_third = df[df['date'] == pre_third_day].reset_index(drop=True)
        pre_data_fourth = df[df['date'] ==pre_fourth_day].reset_index(drop=True)
        pre_data_fifth = df[df['date'] == pre_fifth_day].reset_index(drop=True)


        return data_today, data_first, data_second, data_third, data_fourth, data_fifth, pre_data_first,pre_data_second,pre_data_third, pre_data_fourth, pre_data_fifth
    else:
        return None
