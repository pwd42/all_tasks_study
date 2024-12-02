original_dict = {'apple': 'fruit', 'carrot': 'vegetable', 'banana': 'fruit'}
new_dict = {}

for key, value in original_dict.items():
    new_dict[value] = key

print(new_dict)