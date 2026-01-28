import streamlit as st
import requests

st.title("🌦 Weather Dashboard")

# Input field for city name
city = st.text_input("Enter city name", "Coimbatore")

API_KEY = "YOUR_API_KEY"

if city and API_KEY != "YOUR_API_KEY":
    # Fetch current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "404":
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        # Show city name and weather info directly below input
        st.subheader(f"📍 {city}")
        st.write(f"**Temperature:** {temp} °C")
        st.write(f"**Condition:** {description.capitalize()}")
        st.write(f"**Humidity:** {humidity}%")
        st.write(f"**Wind Speed:** {wind_speed} m/s")
    else:
        st.error("City not found ❌")
else:
    st.info("Please enter a city and set your API key.")
