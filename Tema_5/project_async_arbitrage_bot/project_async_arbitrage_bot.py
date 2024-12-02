import aiohttp
import asyncio
import json

tickers = ("BTC","ETH","SOL","BNB","SUI","APT","PEPE","IMX","OP","ARB","JUP")
spread_target_in_percent = 0.05
url_binance = f"https://api.binance.com/api/v3/ticker/price"
url_kucoin = f"https://api.kucoin.com/api/v1/market/allTickers"

# Функция для выполнения асинхронного запроса.
async def fetch_data(url, session):
    async with session.get(url) as response:
        return await response.json()

# Получение данных с Binance
async def get_binance_data(session):
    prices = {}
    data = await fetch_data(url_binance, session)
    for ticker in tickers:
        for item in data:
            cex_ticker = ticker + "USDT"
            if item["symbol"] == cex_ticker:
                prices[ticker] = item["price"]
    return {"Binance" : prices}

# Получение данных с Kucoin
async def get_kucoin_data(session):
    prices = {}
    data = await fetch_data(url_kucoin, session)
    for ticker in tickers:
        for item in data["data"]["ticker"]:
            cex_ticker = ticker + "-USDT"
            if item["symbol"] == cex_ticker:
                prices[ticker] = item["last"]
    return {"Kucoin" : prices}

# запись в файл
def write_data_to_json_file(name_file, data):
    with open(f"{name_file}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Определение минимальной и максимальной цены и источники бирж
def found_max_spread_prices(data_cexs):
    arbitrage_print_data = {}

    # из-за метода gather() превращаем список словарей в один словарь для дальнейшей обработки данных
    union_data_cexs = {}
    for data_cex in data_cexs:
        union_data_cexs.update(data_cex)

    for ticker in tickers:
        prices = {key: value[ticker] for key, value in union_data_cexs.items()}
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
    return arbitrage_print_data

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

# итоговая асинхронная функция
async def main():
    async with aiohttp.ClientSession() as session:
        # Получаем данные с бирж асинхронно
        tasks = [
            get_binance_data(session),
            get_kucoin_data(session)
        ]
        result_gather = await asyncio.gather(*tasks)

        #запись спарсенных данных в файл
        write_data_to_json_file("result_gather", result_gather)

        # определение минимальной и максимальной цены и источники бирж
        data_for_alert_print = found_max_spread_prices(result_gather)

        # Вывод алерта по заданному порогу спреда
        print_alert_spread(data_for_alert_print, spread_target_in_percent)

# точка запуска программы
if __name__ == "__main__":
    asyncio.run(main())