import requests
import pandas as pd

# 1. Fetch live HKO 9-day forecast
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
res = requests.get(url)
data = res.json()

# 2. Extract forecast items
forecast_list = data.get("weatherForecast", [])
rows = []
for day in forecast_list:
    rows.append({
        "Date": day.get("forecastDate"),
        "Day": day.get("week"),
        "Min Temp (°C)": day.get("forecastMintemp", {}).get("value"),
        "Max Temp (°C)": day.get("forecastMaxtemp", {}).get("value"),
        "Humidity": f"{day.get('forecastMinrh', {}).get('value')}% - {day.get('forecastMaxrh', {}).get('value')}%",
        "Forecast": day.get("forecastWeather")
    })

# 3. Print clean table to GitHub action logs
pd.set_option('display.max_colwidth', None)
df = pd.DataFrame(rows)
print("--- 6:00 AM HKO WEATHER FORECAST ---")
print(df)
