listNumbers = []
for i in range(5):
    i += 1
    listNumbers.append(int(input(f"Введите {i}-ое число: ")))

print(f"Список всех чисел: {listNumbers}")
print(f"Сумма всех чисел: {sum(listNumbers)}")
print(f"Максимальное и минимальное значение в списке: {max(listNumbers)} и {min(listNumbers)}")

