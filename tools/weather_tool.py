import requests

class WeatherTool:
    def __init__(self):
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

    def get_lat_lon(self, city: str):
        response = requests.get(self.geo_url, params={"name": city, "count": 1})
        data = response.json()
        if "results" in data and data["results"]:
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
        return None, None

    def get_weather(self, city: str):
        lat, lon = self.get_lat_lon(city)
        if lat is None or lon is None:
            return f"❌ Could not find weather info for '{city}'."

        response = requests.get(self.weather_url, params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        })
        weather = response.json().get("current_weather", {})
        temperature = weather.get("temperature")

        if temperature is None:
            return "❌ Weather data unavailable."

        suggestion = self.food_suggestion(temperature)
        return (
            f"It is currently {temperature}°C in {city}. "
            f"Based on the weather, it's better to go for {suggestion}."
        )

    def food_suggestion(self, temperature: float) -> str:
        if temperature < 10:
            return "warm and cozy food like soups, curries, or hot chocolate"
        elif 10 <= temperature <= 25:
            return "comfort food such as pasta, stir-fry, or grilled sandwiches"
        else:
            return "light and refreshing options like salads, cold fruits, or yogurt dishes"
