import sys

default_val = 'res\spanish-dict-5-sorted.txt'

def add_plurals(original_path=default_val):
    addition_file = open('res\RAE\CREA_total-plurales-5.txt', 'rt', encoding='utf-8')
    original_file = open(original_path, 'r+', encoding='utf-8')

    originalDict = original_file.read().splitlines()
    additionDict = addition_file.read().splitlines()

    for word in additionDict:
        if word not in originalDict:
            original_file.write(word+'\n')


if __name__ == '__main__':
    add_plurals()