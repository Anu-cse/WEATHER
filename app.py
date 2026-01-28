import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Weather Dashboard using Streamlit
# Author: Anushree (CSE Student)
# -------------------------------

# App title
st.title("🌦 Weather Dashboard")

# Input field for city name
city = st.text_input("Enter city name", "Coimbatore")

# Replace with your OpenWeatherMap API key
API_KEY = "YOUR_API_KEY"

# Function to fetch current weather
def get_current_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    return response.json()

# Function to fetch 5-day forecast
def get_forecast(city, api_key):
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(forecast_url, params=params)
    return response.json()

# Display weather if city is entered
if city and API_KEY != "YOUR_API_KEY":
    data = get_current_weather(city, API_KEY)

    if data.get("cod") != "404":
        # Extract current weather details
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        # Show metrics
        st.subheader("Current Weather")
        st.metric("Temperature (°C)", f"{temp}")
        st.metric("Humidity (%)", f"{humidity}")
        st.metric("Pressure (hPa)", f"{pressure}")
        st.metric("Wind Speed (m/s)", f"{wind_speed}")
        st.write(f"**Condition:** {description.capitalize()}")

        # Fetch forecast data
        forecast_data = get_forecast(city, API_KEY)

        if forecast_data.get("cod") == "200":
            forecast_list = forecast_data["list"]

            # Collect date/time and temperature
            dates = [item["dt_txt"] for item in forecast_list]
            temps = [item["main"]["temp"] for item in forecast_list]

            df = pd.DataFrame({"Date": dates, "Temperature (°C)": temps})

            # Plot forecast
            st.subheader("5-Day Temperature Forecast")
            fig, ax = plt.subplots()
            ax.plot(df["Date"], df["Temperature (°C)"], marker="o", color="blue")
            ax.set_xlabel("Date/Time")
            ax.set_ylabel("Temperature (°C)")
            ax.set_title(f"Temperature Trend for {city}")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.error("Forecast data not available ❌")
    else:
        st.error("City not found ❌")
else:
    st.info("Please enter a city and set your API key to see results.")
