import pandas as pd
from prophet import Prophet
import joblib
import datetime
import requests

URL = 'https://raw.githubusercontent.com/soliharustamxojayeva11-arch/Data-collection/720c180b1165943f356717d1220bd42684b625ba/data.csv'

df = pd.read_csv(URL)

df.columns = df.columns.str.strip()
df['pm25'] = pd.to_numeric(df['pm25'], errors='coerce') 
df = df.dropna(subset=['pm25', 'date'])  


df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])


df_daily = df.groupby(df['date'].dt.date)['pm25'].mean().reset_index()
df_daily = df_daily.rename(columns={'date': 'ds', 'pm25': 'y'})



import logging
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)

model.fit(df_daily)

joblib.dump(model, 'prophet_model.pkl')
print('Model is successfully trained and saved in prophet_model.pkl')
