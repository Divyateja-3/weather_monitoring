import requests
import pymysql
from datetime import datetime,timezone
import time
import json
# Configuration

API_KEY = '5f8f28461419be92b2cf43bcff8319f0' # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
TEMPERATURE_THRESHOLD = 35  # Celsius

# MySQL Database connection
def create_database_connection():
    return pymysql.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='mysql123',  # Replace with your MySQL password
        database='weather_monitoring'
    )

def fetch_weather_data(city):
    response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
    print(f"Response for {city}: {response.status_code} - {response.text}")  # Debugging line
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for {city}: {e}")
            return None
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None
# Fetch weather data


# Process weather data
daily_data = {}

def process_weather_data(data):
    if data:
        timestamp = data['dt']
        date = datetime.fromtimestamp(timestamp, timezone.utc).date()
        main_condition = data['weather'][0]['main']
        temp = data['main']['temp']

    if date not in daily_data:
        daily_data[date] = {
            'temps': [],
            'conditions': []
        }

    daily_data[date]['temps'].append(temp)
    daily_data[date]['conditions'].append(main_condition)

    calculate_daily_summary(date)

def calculate_daily_summary(date):
    if date in daily_data:
        temps = daily_data[date]['temps']
        conditions = daily_data[date]['conditions']

        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        dominant_condition = max(set(conditions), key=conditions.count)

        store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition)

def store_daily_summary(date, avg_temp, max_temp, min_temp, dominant_condition):
    connection = create_database_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO daily_weather_summary (date, average_temp, max_temp, min_temp, dominant_condition)
        VALUES (%s, %s, %s, %s, %s)
    ''', (date, avg_temp, max_temp, min_temp, dominant_condition))
    
    connection.commit()
    cursor.close()
    connection.close()

# Alert mechanism
def check_alerts(city, current_temp):
    if current_temp > TEMPERATURE_THRESHOLD:
        trigger_alert(city, current_temp)

def trigger_alert(city, current_temp):
    alert_time = datetime.now().isoformat()
    connection = create_database_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (alert_time, condition, value)
        VALUES (%s, %s, %s)
    ''', (alert_time, f'Temperature exceeded: {current_temp}', current_temp))
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Alert! {city}: Temperature exceeded {current_temp}°C")

# Collect weather data continuously
def collect_weather_data():
    while True:
        for city in CITIES:
            data = fetch_weather_data(city)
            if data:
                current_temp = data['main']['temp']
                process_weather_data(data)
                check_alerts(city, current_temp)
        time.sleep(300)  # Wait for 5 minutes

import matplotlib.pyplot as plt

def visualize_weather_data():
    connection = create_database_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT date, average_temp, max_temp, min_temp FROM daily_weather_summary")
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    dates, avg_temps, max_temps, min_temps = zip(*data)

    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label='Average Temperature', marker='o')
    plt.plot(dates, max_temps, label='Maximum Temperature', marker='o')
    plt.plot(dates, min_temps, label='Minimum Temperature', marker='o')
    plt.title('Daily Weather Summary')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    collect_weather_data()
