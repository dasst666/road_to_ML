from celery_app import celery_app
import time

@celery_app.task
def hello(name: str) -> str:
    # Симулируем долгую работу
    time.sleep(2)
    return f"Hello, {name}!"

# text = """Когда мы пишем программы, нам часто требуется анализировать текст.
# Например, функция может подсчитывать количество слов, количество символов, а также находить самое длинное слово.
# Это особенно полезно при обработке данных, создании поисковых систем или даже в простых учебных заданиях.

# Некоторые слова могут быть короткими, вроде «кот» или «дом».
# Другие встречаются средние по длине: «программирование», «автоматизация», «алгоритм».
# Но иногда встречаются и настоящие монстры: «суперкалифрагилистикэкспиалидошес», «гиперпараметризация», «ультрамикроскопический».

# Кроме того, важно проверять, как функция работает с пунктуацией: запятыми, точками, тире — ведь текст редко бывает идеально чистым.
# Также стоит учитывать пробелы, переносы строк и разные типы символов: латиницу (например, word), цифры (12345) и даже смешанные формы вроде test_пример123.

# Таким образом, длинный тестовый текст помогает убедиться, что функция работает корректно в любых ситуациях."""


@celery_app.task
def parse_text(text: str):
    symbols_remove = ["!", ",", ".", "?", "@", "+", "-", "/", ">", "<", "%", ":", ";", "-"]
    cleaned_text = []
    symbols_in_text = []
    max_length_word = ""

    splitted_text = text.lower().split()
    for char in splitted_text:
        if char not in symbols_remove:
            cleaned_text.append(char)
        else:
            symbols_in_text.append(char)
        if len(char) > len(max_length_word):
            max_length_word = char
    words_counter = len(cleaned_text)
    unique_words_counter = len(set(cleaned_text))
    symbols_counter = len(symbols_in_text)
    print(cleaned_text)
    return {
            "words count": words_counter, 
            "longest word": max_length_word, 
            "unique words count": unique_words_counter, 
            "symbols count": symbols_counter
            }