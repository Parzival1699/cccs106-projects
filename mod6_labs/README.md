# Weather Application - Module 6 Lab

## Student Information
- **Name**: Lawrence Atienza
- **Student ID**: 231003228
- **Course**: CCCS 106
- **Section**: BSCS-3A

## Project Overview
This project is a dynamic, fully responsive desktop weather application built using the Flet framework for Python. It fetches real-time and forecast data from the OpenWeatherMap API, providing users with current conditions, a 5-day forecast, and several quality-of-life enhancements such as theme switching, unit conversion, and a search history. The application is designed with a modern, dark-themed Material Design aesthetic to ensure a clear and engaging user experience.

## Features Implemented

### Base Features
- [x] City search functionality
- [x] Current weather display
- [x] Temperature, humidity, wind speed
- [x] Weather icons
- [x] Error handling
- [x] Modern UI with Material Design

### Enhanced Features
1. 5-Day Daily Forecast Aggregation and Display

Description of what this feature does: This feature utilizes the OpenWeatherMap 5-day/3-hour forecast endpoint to provide a visualized, daily weather summary. The application processes the 40 raw data points (one every 3 hours) and aggregates them to display the daily high, daily low, and an average temperature, alongside a representative icon and weather description for the entire day.

Why you chose this feature: Providing only the current weather limits the utility of the app. The 5-day forecast is a critical feature for any practical weather application, allowing the user to plan several days in advance.

Challenges faced and how you solved them:

Challenge: The API provides 3-hour data points, not true daily summaries.

Solution: I used the collections.defaultdict to group all 3-hour entries under their respective date key. Python's max() and min() functions were then used on these grouped temperature lists to reliably extract the daily high and low. The weather icon and description were sampled from the midday entry (around 12:00 PM) to best represent the day's peak conditions.

2. Dynamic Temperature Unit Switching (°C / °F)

Description of what this feature does: A toggle switch is provided in the header, allowing users to instantaneously switch the temperature display between Celsius (°C) and Fahrenheit (°F). This conversion affects all displayed temperature values, including the current temperature, "feels like" temperature, and all high/low forecast temperatures.

Why you chose this feature: This feature significantly improves the application's usability across different global regions, catering to users who prefer either the metric or imperial system for temperature readings.

Challenges faced and how you solved them:

Challenge: Ensuring consistency, where every single temperature value on the screen—both current weather and all five forecast cards—updates instantly without the user needing to search again.

Solution: A centralized temp_unit variable and a conversion function (convert_temp) were implemented. The toggle_unit handler was set to call the primary search_weather function upon every change. This forces the application to re-render the UI using the newly selected unit, guaranteeing that all data is displayed correctly.

## Screenshots
![Main Weather Display](<screenshots/mainweatherdisplay.png>)
![5-Day Weather Forecast](<screenshots/5dayforecast.png>)
![Search History Dropdown](<screenshots/recentsearches.png>)
![Temperature Unit Toggle](<screenshots/temperaturetoggle.png>)
![Dark Mode View](<screenshots/darkmode.png>)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/Parzival1699/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env
