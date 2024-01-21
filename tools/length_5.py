import sys
default_val = 'res/english-dict.txt'

def lenght_5(fileName):
    original_file = open(fileName, 'rt')
    new_file = open(fileName.replace('.txt', '-5.txt'), 'w')
    new_file.truncate()

    for word in list(set(original_file.read().splitlines())):
        if len(word) == 5:
            new_file.write(word+'\n')

if __name__ == '__main__':
    try:
        lenght_5(sys.argv[1] if len(sys.argv)==2 else default_val)
    except:
        print('Error: No such file: \''+sys.argv[1]+'\'')