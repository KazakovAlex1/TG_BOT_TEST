import aiohttp
import logging

from config import config


async def convert_currency(amount : float, for_curr : str, to_curr : str) -> str:
    if not config.CURRENCY_API_URL:
        return 'Сервис конвертации сейчас не доступен! Попробуйте позже.'
    
    for_curr = for_curr.upper()
    to_curr = to_curr.upper()
    
    url = config.CURRENCY_API_URL

    logging.info(f'Запрос для конвертации {amount} {for_curr} в {to_curr}.')

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                else:
                    return '❌ Ошибка получения курсов валют'
                
                rates = data['Valute']

                if for_curr not in rates and to_curr not in rates and for_curr != 'RUB' and to_curr != 'RUB':
                    return '❌ Таких валют не существует!'
                elif for_curr not in rates and for_curr != 'RUB':
                    return f'❌ "{for_curr}" такой валюты не существует!'
                elif to_curr not in rates and to_curr != 'RUB':
                    return f'❌ "{to_curr}" такой валюты не существует!'

                if for_curr == 'RUB':
                    from_rate = 1
                else:
                    from_rate = rates[for_curr]['Value']
                
                if to_curr == 'RUB':
                    to_rate = 1
                else:
                    to_rate = rates[to_curr]['Value']

                amount_in_rub = amount * from_rate
                result = amount_in_rub / to_rate
                return f'{amount} {for_curr} = {result:.2f} {to_curr}'
    except aiohttp.ClientTimeout:
        return "⏱️ Таймаут при запросе к ЦБ РФ"
    except aiohttp.ClientError as e:
        logging.error(f"Сетевая ошибка: {e}")
        return "📡 Ошибка соединения с ЦБ РФ"
    except KeyError as e:
        logging.error(f"Ошибка в структуре данных: {e}")
        return "⚠️ Ошибка обработки данных ЦБ РФ"
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
        return "⚠️ Внутренняя ошибка конвертера"