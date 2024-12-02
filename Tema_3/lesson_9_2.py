# мой вариант

# def is_palindrome(str):
#     str_normalized = str.lower().replace(" ", "")
#     str_list =  list(str_normalized)
#     str_list.reverse()
#     str_reversed = "".join(str_list)
#
#     if str_normalized == str_reversed:
#         return True
#     else:
#         return False

# вариант учителя
def is_palindrome(s):
    str_normalized = s.lower().replace(" ", "")
    return str_normalized == str_normalized[::-1]