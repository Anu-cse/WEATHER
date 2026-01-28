import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Title
st.title("🌦 Weather Dashboard with Forecast")

# Input city name
city = st.text_input("Enter city name", "Coimbatore")

# API key (replace with your own from OpenWeatherMap)
api_key = "YOUR_API_KEY"

# Current weather
if city:
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["main"]
        temp = weather["temp"]
        humidity = weather["humidity"]
        pressure = weather["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        st.subheader("Current Weather")
        st.metric("Temperature (°C)", f"{temp}")
        st.metric("Humidity (%)", f"{humidity}")
        st.metric("Pressure (hPa)", f"{pressure}")
        st.metric("Wind Speed (m/s)", f"{wind_speed}")
        st.write(f"**Condition:** {description.capitalize()}")

        # Forecast (5 days, every 3 hours)
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_data["cod"] == "200":
            forecast_list = forecast_data["list"]

            # Extract date, temp
            dates = []
            temps = []
            for item in forecast_list:
                dates.append(item["dt_txt"])
                temps.append(item["main"]["temp"])

            df = pd.DataFrame({"Date": dates, "Temperature (°C)": temps})

            st.subheader("5-Day Temperature Forecast")
            fig = px.line(df, x="Date", y="Temperature (°C)", title=f"Temperature Trend for {city}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Forecast data not available ❌")
    else:
        st.error("City not found ❌")
