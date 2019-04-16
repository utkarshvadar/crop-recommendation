import pandas as pd
import numpy as np

import pickle
import math
import requests
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


import os
BASE = os.path.dirname(os.path.abspath(__file__))
#BASE = ''
regressor = pickle.load(open(os.path.join(BASE,'regressor.sav'), 'rb'))
labelencoder_district = pickle.load(open(os.path.join(BASE,'labelencoder_district.sav'), 'rb'))
labelencoder_crop = pickle.load(open(os.path.join(BASE,'labelencoder_crop.sav'), 'rb'))
labelencoder_season = pickle.load(open(os.path.join(BASE,'labelencoder_season.sav'), 'rb'))
onehotencoder_season = pickle.load(open(os.path.join(BASE,'onehotencoder_season.sav'), 'rb'))


def data_tranform(labelencoder_district,labelencoder_season,labelencoder_crop,onehotencoder_season,data):
    
    
    data[:, 0] = labelencoder_district.transform(data[:, 0])
    data[:, 2] = labelencoder_season.transform(data[:, 2])
    data[:, 5] = labelencoder_crop.transform(data[:, 5])
    data = onehotencoder_season.transform(data).toarray()
    return data
    
def get_climate(district,year,season,crops):

    climate = pd.read_csv(os.path.join(BASE,'climate_avg_season.csv'))
    data = climate[(climate.district==district)&(climate.season==season)].reset_index()
    data['annual_rainfall'] = climate[(climate.district==district)&(climate.season=='Whole Year')].loc[:,'rainfall'].reset_index(drop=True)
    data['year']=year
    df = pd.DataFrame(columns= ['district', 'year', 'season', 'annual_rainfall', 'rainfall', 'Crop','TempH','TempL','TempAvg', 'HumAvg','PAvg'])
    for crop in crops:
        data['Crop'] = crop
        df = pd.concat([df,data.copy()])
    return df.reindex(columns = ['district', 'year', 'season', 'annual_rainfall', 'rainfall', 'Crop','TempH','TempL','TempAvg', 'HumAvg','PAvg'])

def get_price_by_city(city,crops):
    city_low = city
    city = city.upper()
    
    data = pd.read_csv(os.path.join(BASE,'market.csv'))
    city_market = pd.DataFrame(columns= ['district','crop','price'])
    for crop in crops:
        arr = [city_low,crop]
        city_market_crop = data[(data.crop==crop)]
        city_market_crop.model = city_market_crop.model.astype(np.int64)
        if(len(city_market_crop[city_market_crop.city==city]))==0:
            arr.append(city_market_crop['model'].mean())
        else :
            arr.append((city_market_crop[city_market_crop.city==city]['model'].values[0]))
        #print(arr)
        city_market=city_market.append(pd.Series(arr,index = city_market.columns),ignore_index=True)
    return city_market
    
def get_district_by_latlng(lat,lng):
    #address= city+" maharahtra"
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' +str(lat) + ',' +str(lng)+'&key=AIzaSyC0QXKSsqRQWni-55EGzlVBT1RD8kbKC3Q'
    #https://maps.googleapis.com/maps/api/geocode/json?&address=sangli%20maharahtra
    results = requests.get(geocode_url)
        # Results will be in JSON format - convert to dict using requests functionality
    results = results.json()
    
    for ac in results.get('results'):
        for types in ac.get('address_components'):
            if types.get('types')[0] == 'administrative_area_level_2':
                district = types.get('short_name')
                break
    return district
    

crops_code= {
"02002":"Bajra",
"03022":"Urad",
"04005":"Castor seed",
"01001":"Cotton(lint)",
"03006":"Gram",
"03016":"Moong(Green Gram)",
"04003":"Groundnut",
"04007":"Linseed",
"02015":"Maize",
"08046":"Maize",
"10015":"Rapeseed &Mustard",
"03020":"Arhar/Tur",
"02023":"Rice",
"04008":"Safflower",
"04019":"Sesamum",
"02011":"Jowar",
"04017":"Soyabean",
"04018":"Sunflower",
"02009":"Wheat",
"02012":"Wheat"}

crops = list(crops_code.values())

def crop_model(lat,lng,season):
    
    district = get_district_by_latlng(lat,lng)
    if(season=='current'):
        season='Kharif'
    df = get_climate(district.lower(),2014,season,crops)
    
    
    temp = data_tranform(labelencoder_district,labelencoder_season,labelencoder_crop,onehotencoder_season,df.values)
    
    pred = regressor.predict(temp)
    
            
    market_price = get_price_by_city(district.lower(),crops)
    
    profit = market_price['price'].values*pred
    
    profit_df  =  pd.DataFrame({'crop':crops,'profit':profit})
    profit_df=profit_df.sort_values(by=['profit'],ascending=False)
    
    return profit_df.head(5).reset_index(drop=True)
        

