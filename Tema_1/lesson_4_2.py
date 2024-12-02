text = "Я прохожу курсы на крутом сайте ‘AIO STUDY’." \
    "Тут я обучусь программированию на python и коду под web3. Это даст мне в дальнейшем сильный буст." \
    "Тут много домашки, что дает мне хорошую практику. Python - идеальный выбор. Всем успехов!"

symbolsForReplace = ["‘", "’", ".", "!", ",", "-"]
for symbol in symbolsForReplace:
    text = text.replace(symbol, " ")

words = text.lower().split()

countWords = {}
for word in words:
    currentValue = countWords.get(word, 0)
    currentValue += 1
    countWords[word] = currentValue

print(countWords)