import pyautogui
import time
import keyboard
import mouse
import os
import sys

configSet = True
# Import the settings' values from the textfile
try:
    configVals = open('config/values.txt', 'r', encoding='utf-8')
    configVals = configVals.read().split(':')
    language = configVals[0]
    tildes = bool(configVals[1])
    configVals = [int(val) for val in configVals[2:]]
    initX = configVals[0]
    initY = configVals[1]
    letterWidth = letterHeight = configVals[2]
    rgbGrey = (configVals[3], configVals[4], configVals[5])
    rgbYellow = (configVals[6], configVals[7],  configVals[8])
    rgbGreen = (configVals[9], configVals[10],  configVals[11])
except:
    configSet = False

# Configurable settings
startKey = 'shift'
stopKey = 'esc'
letterNum = 5
columnNum = 6

# The proper time delays depend on the duration of the animations of the webpage
# The ones set work perfectly with https://wordlegame.org/es
delay1 = 1
delay2 = 2
delay3 = 3

# Import all the words ordered by the frequencies of their characters from the selected text file
dictWords = None
initialGuess = None
if configSet:
    dictWords = open('res/'+language+'-dict-5-sorted.txt', 'r', encoding='utf-8')
    dictWords = dictWords.read().splitlines()
    initialGuess = dictWords[0]

botStop = False


def wordleBot():
    print('-- Select an option --')
    print('Enter a number:')
    print('1. Solve a word\n2. Configurate the settings\n3. Infinity mode')
    answ = -1
    while answ not in [1, 2, 3]:
        answ = int(input())
        if answ not in [1, 2, 3]:
            print('Invalid option. Try again')
    if answ == 1:
        userGuess = ''
        while userGuess not in dictWords:
            userGuess = input('Enter your initial guess:\n')
            if userGuess not in dictWords:
                print('Unrecognized word. Try again')
        solve(userGuess)
    else:
        if answ == 2:
            config()
        else:
            if answ == 3:
                os.system('cls||clear')
                print('Infinity mode solves infinite words until the script is stopped')
                print('-'*35)
                print('Is highly recommended to use it only on wordlegame.org')
                print('-'*35)
                answ = input('Continue? Y/N\n')
                if answ == 'y' or answ == 'Y':
                    while not botStop:
                        solve(initialGuess)
                        if not botStop:
                            time.sleep(delay3)
                            keyboard.send('enter')
                            time.sleep(delay2)


def stopBot(e):
    global botStop
    if e.event_type == keyboard.KEY_DOWN and e.name == stopKey:
        botStop = True


def config():
    configFile = open('config/values.txt', 'w', encoding='utf-8')
    configFile.truncate()

    os.system('cls||clear')
    printBoxed('config')
    languages = getLanguages()
    print('-- Language selection --')
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
    print('-- Mark letter\'s position and size --')
    print('Left-click your mouse at the corners of the first')
    print('two letters of the first word in the specified order')
    print('Key aspects:')
    print('- It must be inside the square')
    print('- Try to click at the same pixel of each square')
    print('(The script analises the colors from those positions)')
    print('┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐')
    print('│¹W │ │²O │ │ R │ │ D │ │   │')
    print('└───┘ └───┘ └───┘ └───┘ └───┘')
    print('Press \''+startKey+'\' to start recording')
    keyboard.wait(startKey)
    mouse.wait(button='left')
    initPos = mouse.get_position()
    time.sleep(0.1)
    mouse.wait(button='left')
    secPos = mouse.get_position()
    for coord in initPos:
        configFile.write(str(coord)+':')
    configFile.write(str(abs(secPos[0]-initPos[0])))

    os.system('cls||clear')
    print('-- Adjust wordle\'s colors --')    
    print('Left-click your mouse on the tree colors in order')
    print('1. Grey  --  2. Yellow -- 3. Green')
    print('Press \''+startKey+'\' to start recording')
    keyboard.wait(startKey)
    colors = []
    for i in range(3):
        mouse.wait(button='left')
        x, y = mouse.get_position()
        colors.append(pyautogui.pixel(x, y))
        time.sleep(0.1)
    for color in colors:
        for val in color:
            configFile.write(':'+str(val))
    

def getLanguages():
    dirContent = os.listdir('res')
    languages = list(set([title[:title.index('-')].capitalize() for title in dirContent if 'dict' in title]))
    return languages

def solve(guess=initialGuess):
    os.system('cls||clear')
    printBoxed('solve')
    print('-'*35)
    print("  Press '"+startKey+"' to start the bot")
    print("  Keep '"+stopKey+"' pressed to stop")
    print('-'*35+'\n')
    keyboard.wait(startKey)
    
    posY = initY
    letterLists = [[], [], []]
    greyLetters, yellowLetters, greenLetters = letterLists
    checkedWords = []
    win = False

    while not botStop:
        validGuess = False

        while(not validGuess):
            # Ensure the script writes the words in the correct window
            mouse.move(x=initX, y=initY, absolute=True)
            mouse.click(button='left')
            keyboard.write(guess)
            time.sleep(delay1)
            keyboard.send('enter')
            time.sleep(delay2)
            checkedWords.append(guess)
            validGuess = classifyLetters(guess, posY, letterLists)

            if not validGuess:
                for i in range(letterNum):
                    keyboard.send('backspace')
                guess = selectOption(letterLists, checkedWords)

        print("Letter detection:")
        print("Grey: "+', '.join(greyLetters))
        print("Yellow: "+', '.join([yellow.char for yellow in yellowLetters]))
        print("Green: "+', '.join([green.char for green in greenLetters])+'\n')

        posY += letterHeight
        if len(greenLetters) >= letterNum:
            print(" -- WON --\n")
            win = True
            break
        elif posY > initY + letterHeight*columnNum-1:
            print(" -- LOST --\n")
            break

        guess = selectOption(letterLists, checkedWords)
        print("Guess selection:")
        print(guess.upper()+'\n')

        if botStop:
            print("Stopped sucessfully")

    return win


def multiIndexOf(array, element):
    idxs = []
    for i in range(len(array)):
        if array[i] == element:
            idxs.append(i)
    return idxs


def classifyLetters(guess, posY, letterLists):
    greyLetters, yellowLetters, greenLetters = letterLists
    for i in range(letterNum):
        posX = initX + letterWidth*i
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
        # An uncolored last character means character/word recognision failure
        elif i == letterNum-1:
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
    raise Exception("Unable to find any words")


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


if __name__ == '__main__':
    keyboard.hook(stopBot)
    # TODO: Double config when wrong file and config selected
    if not configSet: 
        configInput = input('Error: Configuration parameters not set correctly\nDo you want to set the parameters now? Y/N\n')
        if configInput == 'y' or configInput == 'Y':
            config()
    if configSet or configInput == 'y' or configInput == 'Y':
        if len(sys.argv) > 1:
            if len(sys.argv)==3:
                globals()[sys.argv[1]](sys.argv[2])
            else:
                globals()[sys.argv[1]]()
        else:
            os.system('cls||clear')
            printBoxed('Wordle')
            printBoxed('Auto')
            printBoxed('Solver')
            wordleBot()

    keyboard.unhook_all()
