# Wordle Auto Solver
![](/res/title.png)

> [!WARNING]  
> This script includes code that emulates mouse and keyboard input; run the code with caution.

## Description
This repository contains a Wordle Auto Solver, a tool designed to automate the solving of Wordle puzzles *in any webpage*. The approach used in this solver is inspired by the methods discussed by *Games Computer Play* in his YouTube videos:
- [Simulating Wordle: in search of the perfect strategy](https://youtu.be/ZCSajRqzYyg?si=3bOTbp9qbbUQmoCU)
- [Perfect WORDLE algorithm (and how I found it)](https://youtu.be/sVCe779YC6A?si=_IKnXR-EXDeHmubC)

## Features
- **Algorithmic Approach:** The solver utilizes a character frequency-sorted dictionary and algorithmic techniques outlined in the referenced videos to efficiently deduce potential solutions.

- **Web Compatibility:** It is designed to work seamlessly with any Wordle game interface available online.

- **Terminal-Friendly:** The repository includes scripts that can be run separately in the terminal for executing the solver, configuring settings, or updating dictionaries.

## Get Started
Firstly, make sure that [Python](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) are installed on your system.

Next, download the latest release of the repository from [here](https://github.com/albert-ce/wordle-auto-solver/releases)

Finally, once downloaded, navigate to the main directory in your terminal and install all the needed packages using the given command:

    pip install -r requirements.txt

Now you're ready to use the **Wordle Auto Solver**. Read the instruccions below to start solving.

## Usage Guide
To begin, choose the Wordle webpage you wish to solve and execute the main script from the command line to access the selection menu. You can run it using:

    python .\src\wordle.py

*(The syntax may differ depending on your operating system)*

The first time, you'll need to configure the settings to run any of the code. **You must modify these settings when solving a different Wordle or if the positions of the game's elements on the screen change.** You can do this at any time using:

    python .\src\wordle.py config

After the configuration, you can **solve a Wordle** by selecting the corresponding option in the main script's menu (as mentioned above) or by using:

    python .\src\wordle.py solve <custom first guess>

Alternatively, *(to use the script's default first guess)*:

    python .\src\wordle.py solve

Finally, just make sure to switch to the game's tab before start the solver by pressing 'shift'.

> [!NOTE]  
> The code simulating/recording user input won't run until the 'shift' key is pressed, and you can stop any automated behaviour by pressing 'esc' whenever necessary

## Win Rate Stats
The solver's performance in winning games, tested on [wordlegame.org](https://wordlegame.org/):

|             | English | Spanish | Total      |
|-------------|---------|---------|------------|
| Won         | 722     | 634     | 1356       |
| Played      | 764     | 712     | 1476       |
| Percentatge | 94.50%  | 89.04%  | **91.87%** |

## Solve in Other Languages or Add words
To solve Wordle in languages other than English or Spanish, follow these steps:

1. Obtain a text (.txt) file containing all the words of the desired language from online sources.

2. To be able to select the added language later, add the file to the .\res directory, using a name formatted similarly to others (xxxxx-dict.txt).

3. Next, filter out any non-5 letter words using:

        python .\tools\length_5.py .\res\xxxxx-dict.txt


4. Finally, sort the words appropriately using:

        python .\tools\sort_words.py .\res\xxxxx-dict-5.txt

    Replace xxxxx with the language's name

**If a word is missing in an existent file, simply add it and do the 4th step to sort the modified list of words.**

## Used Resources
This repo uses resources from these external repositories/sites:
- [diccionario-espanol-txt](https://github.com/JorgeDuenasLerin/diccionario-espanol-txt) *by [JorgeDuenasLerin](https://github.com/JorgeDuenasLerin)*
- [english-words](https://github.com/dwyl/english-words/) *by [dwyl](https://github.com/dwyl)*
- [CREA - Listado de frecuencias](hthttps://corpus.rae.es/lfrecuencias.html)