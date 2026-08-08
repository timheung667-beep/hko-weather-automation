import requests

# 1. Fetch live HKO 9-day forecast
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
res = requests.get(url)
data = res.json()

# 2. Extract forecast list
forecast_list = data.get("weatherForecast", [])

# 3. Print each day line-by-line for clear reading in logs
print("--- 6:00 AM HKO WEATHER FORECAST ---\n")

for day in forecast_list:
    date = day.get("forecastDate")
    week = day.get("week")
    min_t = day.get("forecastMintemp", {}).get("value")
    max_t = day.get("forecastMaxtemp", {}).get("value")
    humidity = f"{day.get('forecastMinrh', {}).get('value')}% - {day.get('forecastMaxrh', {}).get('value')}%"
    forecast = day.get("forecastWeather")
    
    print(f"📅 {date} ({week})")
    print(f"   🌡️ Temp: {min_t}°C - {max_t}°C | 💧 Humidity: {humidity}")
    print(f"   ☁️ Forecast: {forecast}\n")
