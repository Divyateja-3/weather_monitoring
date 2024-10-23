# weather_monitoring

# Real-Time Weather Monitoring System

## Overview

This project implements a real-time data processing system for monitoring weather conditions using the OpenWeatherMap API. The system provides summarized insights through rollups and aggregates, focusing on key weather parameters such as temperature and weather conditions.

## Features

- **Real-Time Data Retrieval**: Continuously fetch weather data from the OpenWeatherMap API at configurable intervals.
- **Temperature Conversion**: Convert temperature values from Kelvin to Celsius or Fahrenheit based on user preference.
- **Daily Weather Summary**: Roll up weather data daily and calculate aggregates:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition
- **Alerting Mechanism**: User-configurable thresholds for temperature and specific weather conditions, triggering alerts when thresholds are breached.
- **Visualizations**: Display daily weather summaries, historical trends, and alerts.

## Data Source

The system retrieves data from the [OpenWeatherMap API](https://openweathermap.org/). You will need to sign up for a free API key to access the data.

### API Parameters Used

- **main**: Main weather condition (e.g., Rain, Snow, Clear)
- **temp**: Current temperature in Kelvin
- **feels_like**: Perceived temperature in Kelvin
- **dt**: Time of the data update (Unix timestamp)

## System Requirements

- Python 3.x
- MySQL or any other preferred database
- I used MySQL database
- Docker (optional, for containerization)

## Dependencies

- `requests`: For making API calls
- `pandas`: For data manipulation and analysis
- `matplotlib`: For data visualization (optional)
- `sqlalchemy`: For database interactions

You can install the dependencies using:

```bash
pip install requests pandas matplotlib sqlalchemy
