import requests
from requests import HTTPError

base_url = "https://api.gateio.ws/api/v4/spot/order_book"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
pair_Params = ["BTC_USDT", "ETH_USDT", "SOL_USDT"]

for pairParam in pair_Params:
    query_param = f"currency_pair={pairParam}"
    try:
        response = requests.get(base_url, headers=headers, params=query_param)
        response.raise_for_status() # Выбрасывает исключение для кода 4xx и 5xx
        print(f"Данные для пары {pairParam}:")
        print(response.json())
    except HTTPError as http_err:
        print(f"Ошибка HTTP: {http_err}")
    except Exception as err:
        print(f"Общая ошибка: {err}")