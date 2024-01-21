import pyautogui
import time
import keyboard
import sys

# Configurable settings

# The default settings are set to solve this wordle webpage https://wordlegame.org/es
initX = 1245
initY = 228
letterWidth = letterHeight = 77
rgbGrey = (164, 174, 196)
rgbYellow = (243, 194,  55)
rgbGreen = (121, 184,  81)
initialGuess = "aireo"
startKey = 'shift'
stopKey = 'esc'
letterNum = 5
columnNum = 6
language = 'spanish'

# The proper time delays depend on the duration of the animations of the webpage
# The ones set work perfectly with https://wordlegame.org/es
delay1 = 0.25
delay2 = 1
delay3 = 2

# Import of a text file with all the words ordered by the frequencies of their characters
dictWords = open('res/'+language+'-dict-5-sorted.txt', 'r', encoding='utf-8')
dictWords = dictWords.read().splitlines()

botStop = False


def wordleBot():
    initialPrints()
    while not botStop:
        solve(initialGuess)
        if not botStop:
            time.sleep(delay3)
            pyautogui.press('enter')
            time.sleep(delay2)


def stopBot(e):
    global botStop
    if e.event_type == keyboard.KEY_DOWN and e.name == stopKey:
        botStop = True


def solve(guess=initialGuess):
    posY = initY
    letterLists = [[], [], []]
    greyLetters, yellowLetters, greenLetters = letterLists
    checkedWords = []
    win = False

    while not botStop:
        validGuess = False

        while(not validGuess):
            # Ensure the script writes the words in the correct window
            pyautogui.click(x=initX, y=initY)
            keyboard.write(guess)
            time.sleep(delay1)
            pyautogui.press('enter')
            time.sleep(delay2)
            checkedWords.append(guess)
            validGuess = classifyLetters(guess, posY, letterLists)

            if not validGuess:
                pyautogui.press('backspace', presses=letterNum)
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
        if word not in checkedWords:
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


def initialPrints():
    printBoxed('Wordle')
    printBoxed('Auto')
    printBoxed('Solver')
    print('-'*35)
    print("  Press '"+startKey+"' to start the bot")
    print("  Keep '"+stopKey+"' pressed to stop")
    print('-'*35+'\n')
    keyboard.wait('shift')


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
    try:
        wordleBot()
    finally:
        keyboard.unhook_all()
