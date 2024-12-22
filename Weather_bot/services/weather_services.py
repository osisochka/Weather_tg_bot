import requests
from Weather_bot.services import config
from collections import defaultdict

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



def format_forecast(forecast_data):
    """
    Форматирует прогноз погоды в читабельный вид.
    """
    grouped_data = defaultdict(list)

    for entry in forecast_data:
        date, time = entry["dt_txt"].split(" ")
        grouped_data[date].append((time, entry["main"]["temp"], entry["weather"][0]["description"]))

    formatted_text = ""
    for date, entries in grouped_data.items():
        formatted_text += f"_____________________________\n{date}\n"
        for time, temp, description in entries:
            formatted_text += f"{time[:5]}: {temp}°C, {description}\n"

    return formatted_text


def get_forecast_for_route(route_points, days=3):
    """
    Получает прогноз погоды для маршрута.

    :param route_points: список городов.
    :param days: количество дней прогноза.
    :return: строка с прогнозами.
    """
    forecasts = []
    max_entries = days * 8  # Пример: 8 записей на день (каждые 3 часа)

    for city in route_points:
        lat, lon = get_coordinates(city)
        if lat is None or lon is None:
            forecasts.append(f"Не удалось получить данные для {city}.")
            continue

        weather_data = get_weather_data(city)
        if not weather_data:
            forecasts.append(f"Погода для {city} недоступна.")
            continue

        forecast_text = f"Прогноз для {city} на {days} {'день' if days == 1 else 'дней'}:\n"
        formatted_forecast = format_forecast(weather_data[:max_entries])
        forecast_text += formatted_forecast
        forecasts.append(forecast_text)

    return "\n\n".join(forecasts)




