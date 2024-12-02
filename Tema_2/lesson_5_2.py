import re

with open("input.txt", "r", encoding = "utf-8") as file:
    lines = file.readlines()
    textData = [line.strip() for line in lines]

for index, line in enumerate(lines, start=1):
    count = len(re.findall(r'\w{2,}', line))
    print(f"В {index} строке {count} слов")

# Для корректного и более эффективного подсчета строки можно заменить textData.index(line) на обычный счетчик строк,
# чтобы избежать возможных проблем с одинаковыми строками и многократного поиска индекса.