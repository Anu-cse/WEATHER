import streamlit as st
import requests
import pandas as pd

st.title("🌦 Weather Dashboard with Forecast")

city = st.text_input("Enter city name", "Coimbatore")
API_KEY = "YOUR_API_KEY"

if city and API_KEY != "YOUR_API_KEY":
    # Current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "404":
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        st.subheader("Current Weather")
        st.metric("Temperature (°C)", f"{temp}")
        st.metric("Humidity (%)", f"{humidity}")
        st.metric("Pressure (hPa)", f"{pressure}")
        st.metric("Wind Speed (m/s)", f"{wind_speed}")
        st.write(f"**Condition:** {description.capitalize()}")

        # Forecast
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_data.get("cod") == "200":
            forecast_list = forecast_data["list"]
            dates = [item["dt_txt"] for item in forecast_list]
            temps = [item["main"]["temp"] for item in forecast_list]

            df = pd.DataFrame({"Date": dates, "Temperature (°C)": temps})

            st.subheader("5-Day Temperature Forecast")
            st.line_chart(df.set_index("Date"))
        else:
            st.error("Forecast data not available ❌")
    else:
        st.error("City not found ❌")
