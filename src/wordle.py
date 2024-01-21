import pyautogui
import time
import keyboard
import math

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

letterLists = [[],[],[]]

# Import of a text file with all the words ordered by the frequencies of their characters    
dictWords = open('res/'+language+'-dict-5-sorted.txt', 'r', encoding='utf-8')
dictWords = dictWords.read().splitlines()

botStop = False

def wordleBot():

    print("\nPress '"+startKey+"' to start the bot")
    print("Keep '"+stopKey+"' pressed to stop")
    keyboard.wait('shift')

    while not botStop:

        botWorking(initialGuess)

        if not botStop:
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            global letterLists
            letterLists = [[],[],[]]

def stopBot(e):
    global botStop
    if e.event_type == keyboard.KEY_DOWN and e.name == stopKey:
        botStop = True

def botWorking(initialGuess):
    guess = initialGuess
    posY = initY
    greyLetters, yellowLetters, greenLetters = letterLists
    notExists = []

    while not botStop:

        validGuess = False
        while(not validGuess):
            pyautogui.click(x=initX, y=initY)
            keyboard.write(guess)

            # The proper time delays depend on the duration of the animations of the webpage
            # The ones set work perfectly with https://wordlegame.org/es
            time.sleep(0.25)
            pyautogui.press('enter')
            time.sleep(1)
            validGuess = classifyLetters(guess, posY)
            if not validGuess:
                notExists.append(guess)
                if selectOption(notExists) != None:
                    guess = selectOption(notExists)
                pyautogui.press('backspace', presses=5)

        print("\nLetter detection:")
        print("grey: "+', '.join(greyLetters))
        print("yellow: "+', '.join([yellow.char for yellow in yellowLetters]))
        print("green: "+', '.join([green.char for green in greenLetters])+'\n')

        posY += letterHeight

        if len(greenLetters) >= letterNum:
            print(" -- WON --\n")
            break

        if posY > initY + letterHeight*columnNum-1 and len(greenLetters) < letterNum:
            print(" -- LOST --\n")
            break

        if selectOption(notExists) != None:
            guess = selectOption(notExists)


        print("Guess selection:")
        print(guess.upper())

        if botStop:
            print("Stopped sucessfully")


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


def classifyLetters(guess, posY):
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
            # It must be able to store more than one letter because the same character can have different indexes
            if letterObject not in yellowLetters:
                yellowLetters.append(letterObject)
                if currentChar in greyLetters:
                    greyLetters.remove(currentChar)

        elif color == rgbGreen:
            if letterObject not in greenLetters:
                greenLetters.append(letterObject)
                if currentChar in greyLetters:
                    greyLetters.remove(currentChar)
        else:
            return False
    return True


def multiIndexOf(array, element):
    idxs = []
    for i in range(len(array)):
        if array[i] == element:
            idxs.append(i)
    return idxs


def selectOption(notExists):
    greyLetters, yellowLetters, greenLetters = letterLists
    for word in dictWords:
        if word not in notExists:
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

if __name__ == '__main__':
    keyboard.hook(stopBot)
    try:
        wordleBot()
    finally:
        keyboard.unhook_all()