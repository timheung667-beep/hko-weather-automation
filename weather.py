import requests
import json
from datetime import datetime, timezone, timedelta

# 1. Fetch live HKO 9-day forecast
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
res = requests.get(url)
data = res.json()

forecast_list = data.get("weatherForecast", [])

# 2. Get current Hong Kong Time (UTC+8)
hkt_zone = timezone(timedelta(hours=8))
now = datetime.now(hkt_zone).strftime("%Y-%m-%d %H:%M HKT")

# 3. Save full Markdown table to README.md
md_content = f"# 🌤️ Live Hong Kong Weather Forecast\n\n"
md_content += f"*Last updated automatically: **{now}***\n\n"
md_content += "| Date | Weekday | Temp (°C) | Humidity | Forecast |\n"
md_content += "| :--- | :--- | :--- | :--- | :--- |\n"

for day in forecast_list:
    date = day.get("forecastDate")
    week = day.get("week")
    min_t = day.get("forecastMintemp", {}).get("value")
    max_t = day.get("forecastMaxtemp", {}).get("value")
    humidity = f"{day.get('forecastMinrh', {}).get('value')}% - {day.get('forecastMaxrh', {}).get('value')}%"
    forecast = day.get("forecastWeather")
    
    md_content += f"| {date} | {week} | {min_t}°C - {max_t}°C | {humidity} | {forecast} |\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md_content)

# 4. Save concise JSON data for iOS Scriptable Widget
today = forecast_list[0] if forecast_list else {}
widget_data = {
    "date": today.get("forecastDate", ""),
    "week": today.get("week", ""),
    "temp": f"{today.get('forecastMintemp', {}).get('value', '')}°C - {today.get('forecastMaxtemp', {}).get('value', '')}°C",
    "humidity": f"{today.get('forecastMinrh', {}).get('value', '')}% - {today.get('forecastMaxrh', {}).get('value', '')}%",
    "forecast": today.get("forecastWeather", ""),
    "updated": now
}

with open("today.json", "w", encoding="utf-8") as f:
    json.dump(widget_data, f, indent=2)

print("README.md and today.json updated successfully!")
