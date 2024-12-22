import requests
from Weather_bot.services import config


# Функция для получения координат города
def get_coordinates(city):
    try:
        params = {'q': city, 'appid': config.API_KEY}
        response = requests.get(config.GEOCODE_URL, params=params, timeout=5)
        response.raise_for_status()
        geo_data = response.json()
        if geo_data:
            return geo_data[0]['lat'], geo_data[0]['lon']
        else:
            return None, None
    except Exception as e:
        return None, None


# Функция для получения данных о погоде
def get_weather_data(city):
    try:
        params = {'q': city, 'appid': config.API_KEY, 'units': 'metric'}
        response = requests.get(config.WEATHER_SERVICE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get('list', [])
    except Exception as e:
        return []




def get_forecast_for_route(route_points):
    forecasts = []
    for city in route_points:
        lat, lon = get_coordinates(city)
        if lat is None or lon is None:
            forecasts.append(f"Не удалось получить данные для {city}.")
            continue

        weather_data = get_weather_data(city)
        if not weather_data:
            forecasts.append(f"Погода для {city} недоступна.")
            continue

        forecast_text = f"Прогноз для {city}:\n"
        for entry in weather_data[:3]:  # Ограничиваем до первых 3 записей
            date = entry["dt_txt"]
            temp = entry["main"]["temp"]
            description = entry["weather"][0]["description"]
            forecast_text += f"{date}: {temp}°C, {description}\n"

        forecasts.append(forecast_text)

    return "\n\n".join(forecasts)



