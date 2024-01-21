import sys

default_val = 'res/spanish-dict-5-sorted.txt'

def add_no_accent(file_path):
    new_words = []
    
    file = open(file_path, 'r+', encoding='utf-8')
    lines = file.read().splitlines()

    for word in lines:
        if any(letter in word for letter in ['á', 'é', 'í', 'ó', 'ú']):
            no_accent = word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            if no_accent not in new_words:
                file.write(no_accent+'\n')
                new_words.append(no_accent)
            
        if any(letter in word for letter in ['á', 'é', 'í', 'ó', 'ú', 'ñ']):
            no_accent_n = word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            if no_accent_n not in new_words:
                file.write(no_accent_n+'\n')
                new_words.append(no_accent_n)


if __name__ == '__main__':
    try: 
        add_no_accent(sys.argv[1] if len(sys.argv)==2 else default_val)
    except:
        print('Error: No such file: \''+sys.argv[1]+'\'')