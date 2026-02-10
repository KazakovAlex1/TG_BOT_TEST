import aiohttp
import logging

from config import config


logging.basicConfig(level=logging.INFO)

async def get_weather(city : str) -> str:
    """
    Получает погоду для города через OpenWeatherMap API.
    Args:
        city: Название города (например, 'Москва')
    Returns:
        Строка с информацией о погоде или сообщение об ошибке.
    """
    if not config.WEATHER_API_KEY:
        logging.error('API ключ не найден!')
        return 'Сервис погоды временно не доступен, пожалуйста попробуйте позже.'
    
    url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q' : city,
        'appid' : config.WEATHER_API_KEY,
        'units' : 'metric',
        'lang' : 'ru'
    }

    logging.info(f'Запрос для города: {city}.')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:

                if response.status == 200:
                    data = await response.json()
                    return format_weather_response(data)
                
                elif response.status == 404:
                    return f"🌍 Город '{city}' не найден"
                
                elif response.status == 401:
                    return "❌ Неверный API ключ. Проверьте WEATHER_API_KEY в .env"
                
                else:
                    error_text = await response.text()
                    logging.error(f'API Ошибка: {response.status}:{error_text}')
                    return f"⚠️ Ошибка сервера погоды (код: {response.status})"
    
    except aiohttp.ClientTimeout:
        return "⏱️ Таймаут запроса. Попробуйте позже"
    except aiohttp.ClientError as e:
        logging.error(f"Сетевая ошибка: {e}")
        return "📡 Ошибка соединения с сервером погоды"
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return "⚠️ Внутренняя ошибка"


def format_weather_response(data : dict) -> str:
    try:
        """Форматирует ответ API в читаемый текст."""
        city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']

        return (
                f"🌤️ Погода в {city}:\n"
                f"• {description.capitalize()}\n"
                f"• Температура: {temp}°C\n"
                f"• Ощущается как: {feels_like}°C\n"
                f"• Влажность: {humidity}%\n"
                f"• Ветер: {wind_speed} м/с"
            )
    except KeyError as e:
        logging.error(f"Ошибка парсинга данных: {e}")
        return "⚠️ Не удалось обработать данные о погоде"
