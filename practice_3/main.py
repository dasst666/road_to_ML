# Задача от чатгпт
# Самый базовый вариант подсчета букв
text = "hello"

def parse_string(text: str):
    alphabet_dict = {"h", "e", "l", "o"}
    result = {}
    for char in text:
        cnt = 0
        if char in alphabet_dict:
            if char in result:
                cnt = result[f"{char}"]
                result.update({f"{char}": cnt + 1})
            else:
                cnt += 1
                result.update({f"{char}": cnt})
    return result

print(parse_string(text))

# Просто через Counter встроенный метод подсчета
from collections import Counter
print(Counter(text))


# Более апгрейднутая красивая версия

import string

def parse_string_upgrade(text: str):
    alphabet = set(string.ascii_lowercase)
    result = {}
    for char in text.lower():
        if char in alphabet:
            result[char] = result.get(char, 0) + 1
    return result

print(parse_string_upgrade(text))
