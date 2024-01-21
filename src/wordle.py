import pyautogui
import time
import keyboard

# Import of a text file with all the words ordered by frequency of usage/popularity
dictWords = open('res/spanish-dict-5-sorted.txt', 'r', encoding='utf-8')
dictWords = dictWords.read().splitlines()


# Configurable settings
    
# The default settings are set to solve this wordle webpage https://wordlegame.org/es
initX = 1245
initY = 228
letterWidth = 77
letterHeight = 77
rgbGrey = [164, 174, 196]
rgbYellow = [243, 194,  55]
rgbGreen = [121, 184,  81]
initialGuess = "aireo"
startKey = 'shift'
stopKey = 'capslock'

greyLetters = []
yellowLetters = []
greenLetters = []

botStop = False


def botWorking(initialGuess):
    global botStop
    guess = initialGuess
    posY = initY

    while not botStop:

        if keyboard.is_pressed(stopKey):
            botStop = True

        pyautogui.click(x=initX, y=initY)
        keyboard.write(guess)

        # The proper time delays depend on the duration of the animations of the webpage
        # The ones set work perfectly with https://wordlegame.org/es
        time.sleep(0.25)
        pyautogui.press('enter')
        time.sleep(1)
        classifyLetters(guess, posY)

        print("\nLetter detection:")
        print("grey:", ', '.join(greyLetters))
        print("yellow: ", end='')
        for yellow in yellowLetters:
            print(yellow.char, end=', ')
        print("\ngreen: ", end='')
        for green in greenLetters:
            print(green.char, end=', ')

        posY += letterHeight

        if len(greenLetters) >= 5:
            print("\n\n -- WON --")
            break

        if posY > initY + letterHeight*5 and len(greenLetters) < 5:
            print("\n\n -- LOST --")
            break

        if selectOption(guess) != None:
            guess = selectOption(guess)

        print("\n\nGuess selection:")
        print(guess.upper())

        if botStop:
            print("\nStopped sucessfully")


class letter:
    def __init__(self, char, index):
        self.char = char
        self.index = index


def readPixel(posX, posY):
    pix = pyautogui.pixel(posX, posY)
    color = [pix[0], pix[1], pix[2]]
    return color


def classifyLetters(guess, posY):

    for i in range(5):
        posX = initX + letterWidth*i
        color = readPixel(posX, posY)
        currentLetter = guess[i]
        letterObject = letter(guess[i], i)
        yellowChars = [yellow.char for yellow in yellowLetters]
        greenChars = [green.char for green in greenLetters]
        greenIdxs = [green.index for green in greenLetters]

        if color == rgbGrey:
            if currentLetter not in greyLetters and currentLetter not in yellowChars and currentLetter not in greenChars:
                greyLetters.append(currentLetter)

        elif color == rgbYellow:
            # It must be able to store more than one letter because the same character can have different indexes
            yellowLetters.append(letterObject)
            if currentLetter in greyLetters:
                greyLetters.remove(currentLetter)

        elif color == rgbGreen:
            # It mustn't be able to store more than one letter in the same position
            if i not in greenIdxs:
                greenLetters.append(letterObject)
                if currentLetter in greyLetters:
                    greyLetters.remove(currentLetter)


def multiIndexOf(array, element):
    idxs = []
    for i in range(len(array)):
        if array[i] == element:
            idxs.append(i)
    return idxs


def selectOption(guessCheck):
    for word in dictWords:
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
                    if word != guessCheck:
                        return word


print("\nPress '"+startKey+"' to start the bot")
print("Keep '"+stopKey+"' pressed to stop")
keyboard.wait('shift')

while not botStop:

    botWorking(initialGuess)

    if not botStop:
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)
        greyLetters = []
        yellowLetters = []
        greenLetters = []
