numberText = ""

while not numberText.isdigit():
    numberText = (input("Введите число: "))
    try:
        number = int(numberText)
    except ValueError:
        print("Ошибка: введенное значение не является числом. Попробуйте еще раз.")

print(number)