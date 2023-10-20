import os
os.system('cls')
# coding=utf-8
# input: array with multiple strings
# expected output: rank of the 3 most often repeated words in given set of strings and number of times they occured, case insensitive
# Good luck! You can write all the code in this file.
# Example result:
# 1. "mam" - 12
# 2. "tak" - 5
# 3. "z" - 2

sentences = [
    'Taki mamy klimat',
    'Wszędzie dobrze ale w domu najlepiej',
    'Wyskoczył jak Filip z konopii',
    'Gdzie kucharek sześć tam nie ma co jeść',
    'Nie ma to jak w domu',
    'Konduktorze łaskawy zabierz nas do Warszawy',
    'Jeżeli nie zjesz obiadu to nie dostaniesz deseru',
    'Bez pracy nie ma kołaczy',
    'Kto sieje wiatr ten zbiera burzę',
    'Być szybkim jak wiatr',
    'Kopać pod kimś dołki',
    'Gdzie raki zimują',
    'Gdzie pieprz rośnie',
    'Swoją drogą to gdzie rośnie pieprz?',
    'Mam nadzieję, że poradzisz sobie z tym zadaniem bez problemu',
    'Nie powinno sprawić żadnego problemu, bo Google jest dozwolony',
]

words = [word.lower() for sentence in sentences for word in sentence.split()] # Append all words into one list
words_count = {}

def count_key(key): # Increment value for given key
    if key in words_count.keys():
        words_count[key] += 1
    else:
        words_count[key] = 1

for word in words:
    count_key(word)

sorted_words_count = sorted(words_count.items(), key=lambda x:x[1], reverse=True) # Sort values in words_count
most_common_words = dict(sorted_words_count[:3])

for index, item in enumerate(most_common_words.items()):
    print(f"{index+1}. \"{item[0]}\" - {item[1]}")


