import pyautogui
import time
import keyboard
import mouse
import os
import sys

# Configurable settings
startKey = 'shift'
stopKey = 'esc'
letterNum = 5
columnNum = 6

# The proper time delays depend on the duration of the animations of the webpage
# The ones set work perfectly in many webpages, including
# https://www.nytimes.com/games/wordle/index.html
# https://wordlegame.org/

writeDelay = 0.25
colorDelay = 1.8
restartDelay = 2

botStopped = False


def config():
    configFile = open('config/values.txt', 'w', encoding='utf-8')
    configFile.truncate()

    os.system('cls||clear')
    printBoxed('config')
    languages = getLanguages()
    print('Language selection')
    print('-'*35)
    print('Enter number:')
    for i, lan in enumerate(languages):
        print(str(i+1)+'. '+lan)
    lan = languages[int(input())-1].lower()
    configFile.write(lan+':')
    if lan == 'spanish':
        tildes = input('Tildes? Y/N\n')
    if lan == 'spanish' and (tildes == 'y' or tildes == 'Y'):
        configFile.write('1:')
    else:
        configFile.write('0:')

    os.system('cls||clear')
    print('Mark letter\'s position and size')
    print('-'*53)
    print('Left-click your mouse at the corners of the first')
    print('two letters of the first word in the specified order.')
    print('-'*53)
    print('Key aspects:')
    print('- It must be inside the square')
    print('- Try to click at the same pixel of each square')
    print('* The script extracts colors and maps positions from those points')
    print('┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐')
    print('│¹W │ │²O │ │ R │ │ D │ │ S │')
    print('└───┘ └───┘ └───┘ └───┘ └───┘')
    print('Press \''+startKey+'\' to start recording clicks')
    keyboard.wait(startKey)
    mouse.wait(button='left')
    initPos = mouse.get_position()
    time.sleep(0.2)
    mouse.wait(button='left')
    secPos = mouse.get_position()
    for coord in initPos:
        configFile.write(str(coord)+':')
    configFile.write(str(abs(secPos[0]-initPos[0])))

    os.system('cls||clear')
    print('Adjust wordle\'s colors')
    print('-'*51)
    print('Left-click your mouse on the tree colors in order.')
    print('Tip: You may find them in the \'How to play\' section.')
    print('-'*51)
    print('1st -- Grey\n2nd -- Yellow\n3rd -- Green')
    print('Press \''+startKey+'\' to start recording clicks')
    keyboard.wait(startKey)
    colors = []
    for i in range(3):
        mouse.wait(button='left')
        x, y = mouse.get_position()
        colors.append(pyautogui.pixel(x, y))
        time.sleep(0.2)
    for color in colors:
        for val in color:
            configFile.write(':'+str(val))

    configFile.close()
    os.system('cls||clear')
    print('Settings set successfully')


def getLanguages():
    dirContent = os.listdir('res')
    languages = [title[:title.index('-')].capitalize() for title in dirContent if 'dict' in title]
    languages = sorted(set(languages))
    return languages


def printBoxed(word):
    word = word.upper()
    for letter in word:
        print('┌───┐ ', end='')
    print()
    for letter in word:
        print('│ {} │ '.format(letter), end='')
    print()
    for letter in word:
        print('└───┘ ', end='')
    print()


# Script starts here
# Import the settings' values from the textfile
try:
    configFile = open('config/values.txt', 'r', encoding='utf-8')
    configVals = configFile.read().split(':')
    language = configVals[0]
    tildes = bool(int(configVals[1]))
    configVals = [int(val) for val in configVals[2:]]
    initX = configVals[0]
    initY = configVals[1]
    letterWidth = letterHeight = configVals[2]
    rgbGrey = (configVals[3], configVals[4], configVals[5])
    rgbYellow = (configVals[6], configVals[7],  configVals[8])
    rgbGreen = (configVals[9], configVals[10],  configVals[11])
    configFile.close()

    # Import all the words ordered by the frequencies of their characters from the selected text file
    dictFile = open('res/'+language+'-dict-5-sorted.txt', 'r', encoding='utf-8')
    dictWords = dictFile.read().splitlines()
    defaultGuess = dictWords[0]
except:
    configInput = input('Error: Configuration parameters not set correctly\n' +
                        'Do you want to set the parameters now? Y/N\n')
    if configInput == 'y' or configInput == 'Y':
        config()
        sys.exit('Run the last command again to proceed')
    sys.exit('Exited succesfully')


def wordleBot():
    print('-- Select an option --')
    print('Enter a number:')
    print('1. Solve a word\n2. Configurate the settings\n3. Infinity mode\n4. Exit')
    answ = int(input())
    while answ not in [1, 2, 3, 4]:
        print('Invalid option. Try again')
        answ = int(input())
    if answ == 1:
        userGuess = input('Input your initial guess (Press \'enter\' for default):\n')
        while userGuess not in dictWords and userGuess != '':
            print('Unrecognized word. Try again')
        if userGuess != '':
            solve(userGuess)
        else:
            solve()
    else:
        if answ == 2:
            config()
        else:
            if answ == 3:
                os.system('cls||clear')
                print('Infinity mode solves infinite words until the script is stopped')
                print('-'*63)
                print('Warning: Exclusively for solving the game on wordlegame.org')
                print('-'*63)
                answ = input('Continue? Y/N\n')
                if answ == 'y' or answ == 'Y':
                    gamesNum = 0
                    winNum = 0
                    try:
                        winNum = winNum + solve()
                        while not botStopped:
                            gamesNum = gamesNum + 1
                            time.sleep(restartDelay)
                            keyboard.send('enter')
                            time.sleep(restartDelay/2)
                            winNum = winNum + solve(singleSolve=False)
                    finally:
                        print('Number of wins: '+str(winNum)+'/'+str(gamesNum) +
                            ' --> '+(str(winNum/gamesNum*100) if gamesNum != 0 else '0')+'%')
            else:
                sys.exit('Exited successfully')


def solve(guess=defaultGuess, singleSolve=True):
    if singleSolve:
        os.system('cls||clear')
        printBoxed('solve')
        print('Switch to Wordle\'s tab, then:')
        print('-'*41)
        print("Press '"+startKey+"' to start the bot")
        print("Press '"+stopKey+"' anytime to stop writing words")
        print('-'*41)
        keyboard.wait(startKey)

    guessNum = 0
    letterLists = [[], [], []]
    greyLetters, yellowLetters, greenLetters = letterLists
    checkedWords = []
    win = False

    # Ensure the script writes the words in the correct window
    mouse.move(x=initX, y=initY, absolute=True)
    mouse.click(button='left')

    while not botStopped and guessNum < columnNum and not win:

        validGuess = False
        while not validGuess and not botStopped:
            print("Guess selected:")
            print(guess.upper()+'\n')
            keyboard.write(guess)
            time.sleep(writeDelay)
            keyboard.send('enter')
            time.sleep(colorDelay)
            checkedWords.append(guess)
            validGuess = classifyLetters(guess, guessNum, letterLists)
            if not validGuess:
                for i in range(letterNum):
                    keyboard.send('backspace')
                guess = selectOption(letterLists, checkedWords)

        guessNum = guessNum + 1
        win = len(greenLetters) >= letterNum

        print("Letter detection:")
        print("Grey: "+', '.join(greyLetters))
        print("Yellow: "+', '.join([yellow.char for yellow in yellowLetters]))
        print("Green: "+', '.join([green.char for green in greenLetters])+'\n')

        if not win:
            guess = selectOption(letterLists, checkedWords)
    
    if not botStopped:
        if win:
            print(" -- WON --\n")
        else:
            print(" -- LOST --\n")

    return win


def classifyLetters(guess, guessNum, letterLists):
    greyLetters, yellowLetters, greenLetters = letterLists
    for i in range(letterNum):
        posX = initX + i*letterWidth
        posY = initY + guessNum*letterHeight
        color = pyautogui.pixel(posX, posY)
        currentChar = guess[i]
        letterObject = letter(guess[i], i)

        if color == rgbGrey:
            if currentChar not in greyLetters and currentChar not in yellowLetters and currentChar not in greenLetters:
                greyLetters.append(currentChar)

        elif color == rgbYellow:
            # It must be able to store same characters with different indexes
            if letterObject not in yellowLetters:
                yellowLetters.append(letterObject)
                if currentChar in greyLetters:
                    greyLetters.remove(currentChar)

        elif color == rgbGreen:
            if letterObject not in greenLetters:
                greenLetters.append(letterObject)
                if currentChar in greyLetters:
                    greyLetters.remove(currentChar)
        # An uncolored first character means character/word recognision failure
        elif i == 0:
            return False
    return True


def selectOption(letterLists, checkedWords):
    greyLetters, yellowLetters, greenLetters = letterLists
    for word in dictWords:
        if word not in checkedWords and (tildes or not any(letter in word for letter in ['á', 'é', 'í', 'ó', 'ú'])):
            for grey in greyLetters:
                if grey in word:
                    break
            else:
                for yellow in yellowLetters:
                    if yellow.char not in word:
                        break
                    elif yellow.index in multiIndexOf(word, yellow.char):
                        break
                else:
                    for green in greenLetters:
                        if green.char not in word:
                            break
                        elif green.index not in multiIndexOf(word, green.char):
                            break
                    else:
                        return word
    # All words checked, none returned
    sys.exit('Error: Unable to find any words\n' +
             'This error may be caused by:\n' +
             '- Incorrect color identification\n' +
             '- Incomplete dictionary')


def multiIndexOf(array, element):
    idxs = []
    for i in range(len(array)):
        if array[i] == element:
            idxs.append(i)
    return idxs


class letter:
    def __init__(self, char, index):
        self.char = char
        self.index = index

    def __eq__(self, other):
        if isinstance(other, letter):
            return self.char == other.char and self.index == other.index
        elif isinstance(other, str):
            return self.char == other
        else:
            return False

    def __hash__(self):
        return hash((self.char, self.index))

    def __contains__(self, char):
        if isinstance(char, str):
            return self.char == char
        else:
            return False


def botStop():
    global botStopped
    botStopped = True


keyboard.add_hotkey(stopKey, botStop)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            globals()[sys.argv[1]](sys.argv[2])
        else:
            globals()[sys.argv[1]]()
    else:
        os.system('cls||clear')
        printBoxed('Wordle')
        printBoxed('Auto')
        printBoxed('Solver')
        wordleBot()
    dictFile.close()
    if botStopped:
        print('Stopped successfully')
