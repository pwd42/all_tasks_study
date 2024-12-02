def calculate_average(numbers):
    if len(numbers) > 0:
        try:
            return sum(numbers) / len(numbers)
        except TypeError:
            print("Ошибка входных данных")
    else:
        print("Список пуст, невозможно вычислить среднее значение.")