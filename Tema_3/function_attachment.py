#
# # Пример функции, которая вычисляет квадрат числа
# def square(x):
#     return x * x
# #
# #
# print(square(5))  # Вывод: 25
#
#
# def greet(name):
#     return f"Hello, {name}!"
#
#
# print(greet("Alice"))  # Вывод: Hello, Alice!

#
#
# def add(a, b):
#     return a + b
#
#
# result = add(3, 4)
#
# print(result)  # Вывод: 7
#
# x = 10  # Глобальная переменная
#
#
# def example():
#     x = 5  # Локальная переменная
#     print(x)
#
#
# example()  # Вывод: 5
# print(x)  # Вывод: 10
# #
# x = 10
#
#
# def example():
#     global x
#     x = 5
#
#
# example()
# print(x)  # Вывод:
#
#
# def example():
#     y = 5  # Локальная переменная
#     print(y)
#
#
# example()
#
#
#
#
# def no_return():
#     print("This function returns nothing")
#
# result = no_return()
# print(result)  # Вывод: None
#
#

def process_data(data):
    filtered_data = [x for x in data if x > 0]
    sorted_data = sorted(filtered_data)
    return sorted_data


data = [3, -1, 2, 0, -3, 5]
result = process_data(data)
print(result)

