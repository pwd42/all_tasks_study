import requests
from requests import HTTPError
import json

tickers = ("BTC","ETH","SOL","BNB","SUI","APT","PEPE","IMX","OP","ARB","JUP")
url_binance = f"https://api.binance.com/api/v3/ticker/price"
url_kucoin = f"https://api.kucoin.com/api/v1/market/allTickers"
urls_cex = {"Binance": url_binance, "Kucoin": url_kucoin}
spread_target_in_percent = 0.05

#выполнение запроса по урлу, возврат json
def make_request_by_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f"Ошибка HTTP {url}: {http_err}")
    except Exception as err:
            print(f"Общая ошибка {url}: {err}")

# запись данных словаря в файл json
def write_parsing_json_file(data_file, name_file):
    with open(f"{name_file}.json", "w", encoding = "utf-8") as file:
        json.dump(data_file, file, ensure_ascii=False, indent=4)

#  парсинг цен нужных тикеров с бирж, возвращает словарь
def parsing_actual_price_by_cex(response_def, tickers_def, cex):
    filtered_data_price = {}
    for ticker in tickers_def:
        if cex == "Binance":
            ticker_binance = ticker + "USDT"
            for i in range(len(response_def) - 1):
                if response_def[i]["symbol"] == ticker_binance:
                    filtered_data_price[ticker] = float(response_def[i]["price"])
        elif cex == "Kucoin":
            ticker_kucoin = ticker + "-USDT"
            for i in range(len(response_def["data"]["ticker"]) - 1):
                if response_def["data"]["ticker"][i]["symbol"] == ticker_kucoin:
                    filtered_data_price[ticker] = float(response_def["data"]["ticker"][i]["last"])
    return filtered_data_price

# чтение файла, возврат словаря
def read_file_by_json(name_file):
    try:
        with open(f"{name_file}.json", "r", encoding="utf-8") as file:
            data_read = json.load(file)
            return data_read
    except FileNotFoundError:
        print("Файл не найден")

#Подсчет спреда в процентах и абсолютно
def compute_spread_in_percent(price_1, price_2):
    try:
        spread = compute_spread_abs(price_1, price_2) * 100 / min(float(price_1), float(price_2))
        return round(spread, 6)
    except ValueError:
        print("Неправильный тип данных")
        return None  # Добавление явного возвращаемого значения при ошибке
def compute_spread_abs(price_1,  price_2):
    try:
        return abs(float(price_1) - float(price_2))
    except ValueError:
        print("Неправильный тип данных")
        return None  # Добавление явного возвращаемого значения при ошибке

#определение минимальной и максимальной цены и источники бирж, вывод словаря (мой вариант)
def found_max_spread_prices_2(data_cexs):
    arbitrage_print_data ={}

    for ticker in tickers:
        price_list = []

        for key,value in data_cexs.items():
            price_list.append(value[ticker])
        arbitrage_print_data[ticker] = {}

        for key,value in data_cexs.items():
            if value[ticker] == min(price_list) and min(price_list) != max(price_list):
                arbitrage_print_data[ticker]["cex_from"] = key
                arbitrage_print_data[ticker]["price_min"] = str(value[ticker])
            elif value[ticker] == max(price_list) and min(price_list) != max(price_list):
                arbitrage_print_data[ticker]["cex_to"] = key
                arbitrage_print_data[ticker]["price_max"] = str(value[ticker])
            elif min(price_list) == max(price_list):
                arbitrage_print_data[ticker]["cex_from"] = "Равные значения у бирж"
                arbitrage_print_data[ticker]["cex_to"] = "Равные значения у бирж"
                arbitrage_print_data[ticker]["price_min"] =  min(price_list)
                arbitrage_print_data[ticker]["price_max"] = max(price_list)
        price_list.clear()
    return arbitrage_print_data

# (вариант учителя) - "Вместо постоянного создания и очистки можно избавиться от промежуточного списка и
# сразу сравнивать минимальные и максимальные цены в ходе работы"

def found_max_spread_prices(data_cexs):
    print(data_cexs)
    arbitrage_print_data = {}
    for ticker in tickers:
        prices = {key: value[ticker] for key, value in data_cexs.items()}
        min_cex, min_price = min(prices.items(), key=lambda x: x[1])
        max_cex, max_price = max(prices.items(), key=lambda x: x[1])

        if min_price != max_price:
            arbitrage_print_data[ticker] = {
                "cex_from": min_cex,
                "price_min": str(min_price),
                "cex_to": max_cex,
                "price_max": str(max_price)
            }
        else:
            arbitrage_print_data[ticker] = {
                "cex_from": "Равные значения у бирж",
                "cex_to": "Равные значения у бирж",
                "price_min": str(min_price),
                "price_max": str(max_price)
            }
    print(prices)
    return arbitrage_print_data

# Вывод алерта по заданному порогу спреда
def print_alert_spread(dict_max_spread_prices, spread_target_in_percent_def):
    for key,value in dict_max_spread_prices.items():
        spread_in_percent_current = compute_spread_in_percent(value["price_max"], value["price_min"])
        if spread_in_percent_current > spread_target_in_percent_def:
            print(f'Нашел спред на монете {key} с {value["cex_from"]} на {value["cex_to"]}.')
            print(f'Покупка: {value["price_min"]} $')
            print(f'Продажа: {value["price_max"]} $')
            print(f'Профит: {round(compute_spread_abs(value["price_max"], value["price_min"]), 6)} $')
            print(f'Заданный порог спреда: {spread_target_in_percent_def} %')
            print(f'Текущий спред: {spread_in_percent_current} %\n')

#выполнение программы
arbitrage_parsing_data = {}
for key,value in urls_cex.items():
    # выполнения запроса по урлу
    response = make_request_by_url(value)

    # парсинг цен нужных тикетов с бирж
    data_parsing = parsing_actual_price_by_cex(response, tickers, key)

    # запись данных словаря в файлы json по биржам
    write_parsing_json_file(data_parsing, key)

    # чтение спарсенных данных и запись в общий словарь
    arbitrage_parsing_data[key] = read_file_by_json(key)

#определение минимальной и максимальной цены и источники бирж
data_for_alert_print = found_max_spread_prices(arbitrage_parsing_data)

# Вывод алерта по заданному порогу спреда
print_alert_spread(data_for_alert_print, spread_target_in_percent)
