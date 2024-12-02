import asyncio
import json

from Tema_5.project_await_parser_okx.requestsUtil.InstrumentsRequest import InstrumentsRequest
from Tema_5.project_await_parser_okx.requestsUtil.PriceLimitRequest import PriceLimitRequest

# функции работы с файлами
def write_json_file(name_file, data):
    with open(f"{name_file}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def read_json_file(name_file):
    with open(f"{name_file}.json", "r", encoding="utf-8") as file:
        return json.load(file)
#извлечение тикеров с суффиксом USDT
def extract_needed_tickers(data):
    result_tickers = []
    for i in range(len(data["data"]) - 1):
        suffix = "-USDT"
        current_ticker = data["data"][i]["instId"]
        if suffix in current_ticker:
            result_tickers.append(current_ticker)
    return result_tickers

# выполненеи программы
async def main():
    name_file = "OKX"
    tasks = []
    result_prices = {}

    # запись первичных данных
    instruments_request = InstrumentsRequest()
    task_1 = asyncio.create_task(instruments_request.make_session_and_request())
    result_data_task_1 = await task_1
    write_json_file(name_file, result_data_task_1)

    # чтение с файла и фильтрация тикетов,запись в словарь
    filtered_tickets = extract_needed_tickers(read_json_file(name_file))

    # выполнение асинхронных запросов по каждому тикету
    for ticket in filtered_tickets:
        price_limit_request = PriceLimitRequest(ticket)
        tasks.append(asyncio.create_task(price_limit_request.make_session_and_request()))
    responses = await asyncio.gather(*tasks)

    # итоговая запись цен по каждому тикету в файл
    for response in responses:
        if len(response["data"]) > 0:
            limit_prices = {"buyLmt": response["data"][0]["buyLmt"], "sellLmt": response["data"][0]["sellLmt"]}
            result_prices[response["data"][0]["instId"]] = limit_prices
    write_json_file("result_prices", result_prices)

asyncio.run(main())
