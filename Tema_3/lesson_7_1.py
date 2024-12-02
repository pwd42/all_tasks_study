lines = []

while len(lines) == 0:
    pathFromUser = input("Укажите путь файла: ")
    try:
        with open(pathFromUser, "r", encoding = "utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Файл по указанному пути не найден. Пожалуйста, проверьте путь и повторите попытку.")