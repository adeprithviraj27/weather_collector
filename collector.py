import os
import time
from datetime import datetime
import pandas as pd
import requests
import schedule

CITY = "Pune"
CSV_FILE = "weather_log.csv"


def log_weather():
    url = f"https://wttr.in/{CITY}?format=j1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current = data["current_condition"][0]

        new_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "City": CITY,
            "Temperature_C": float(current["temp_C"]),
            "Condition": current["weatherDesc"][0]["value"],
            "Humidity_%": int(current["humidity"]),
            "Wind_Speed_Kmph": int(current["windspeedKmph"]),
        }

        df_new = pd.DataFrame([new_entry])

        if os.path.exists(CSV_FILE):
            df_new.to_csv(CSV_FILE, mode="a", header=False, index=False)
        else:
            df_new.to_csv(CSV_FILE, mode="w", header=True, index=False)

        print(
            f"[{new_entry['Timestamp']}] Weather data for {CITY} logged successfully!"
        )
    else:
        print(
            f"Failed to fetch weather data. Status code: {response.status_code}"
        )


# Run once immediately on start
log_weather()

# Schedule to run every 10 seconds (change to schedule.every().hour.do(log_weather) for hourly runs)
schedule.every(10).seconds.do(log_weather)

print("Automated Weather Collector running... Press Ctrl + C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)