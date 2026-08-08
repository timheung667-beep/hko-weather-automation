import requests
from datetime import datetime, timezone, timedelta

# 1. Fetch live HKO 9-day forecast
url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
res = requests.get(url)
data = res.json()

forecast_list = data.get("weatherForecast", [])

# 2. Build Markdown text for README.md
hkt_zone = timezone(timedelta(hours=8))
now = datetime.now(hkt_zone).strftime("%Y-%m-%d %H:%M HKT")

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

# 3. Save directly to README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("README.md updated successfully!")
