original_dict = {'apple': 'fruit', 'carrot': 'vegetable', 'banana': 'fruit'}
reversed_original_dict = {value: key for key, value in original_dict.items()}
print(reversed_original_dict)

# дополнительное задание
reverse_dict_2 = {
    value: [key for key, val in original_dict.items() if val == value]
    if list(original_dict.values()).count(value) > 1 else key
    for key, value in original_dict.items()
}

print(reverse_dict_2)
