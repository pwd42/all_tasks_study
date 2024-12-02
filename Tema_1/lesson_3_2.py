listNumbers = []
for i in range(5):
    i += 1
    listNumbers.append(int(input(f"Введите {i}-ое число кортежа: ")))

tupleNumbers = tuple(listNumbers)

print(f"\nПервый и последний элемент кортежа - {tupleNumbers[0]} и {tupleNumbers[len(tupleNumbers) - 1]}")
print(f"Длина кортежа - {len(tupleNumbers)}")
print(f"Сумма всех чисел в кортеже - {sum(tupleNumbers)}")

checkNumber = int(input("\nВведите число для проверки в кортеже "))

if checkNumber in tupleNumbers:
  print(f"Число {checkNumber} содержится в кортеже, его индекс {tupleNumbers.index(checkNumber)}")
else:
    print(f"\nЧисло {checkNumber} не содержится в кортеже")

# можно улучшить - контроль того, что пользователь действительно вводит числа в консоль,
# а не другие символы (подсказка: сделать это можно через строковый метод a.isdigit(), где а - переменная типа string)