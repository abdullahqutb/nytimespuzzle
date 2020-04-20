# Instructions to run--------------------------------------------------------------------------------------
# In ubuntu/linux:
# Make sure to install python3 and Mozilla Firefox in your environment
# Open Terminal in the directory this file is located in
# Type: python3 guiFinal.py
# Instructions to run --------------------------------------------------------------------------------------

# @desc: This program creates a GUI from the data given by filename "file.txt"
#       Just rename the data to "file.txt" and type make data in terminal
#
# @author: Sayed Abdullah Qutb
# @date: 21/04/2020
# @version: v2.0
#

# Import the tkinter library for the gui
import tkinter as tk
import time
import datetime

cellSize = 75
# Creating the grid table of the puzzle
def createTable():
    i = 0
    while i <= 5 * cellSize:
        j = 0
        while j <= 5 * cellSize:
            W.create_rectangle(i, j, cellSize, cellSize, outline='black')
            j+=cellSize
        i+=cellSize
    return

# Marking numbers based on clues
numSize = 15
def markNum(j, i, num):
    x = cellSize * i + 10
    y = cellSize * j + 12
    W.create_text(x, y, font=("Arial", numSize), text = num)
    return

# Writing letters in cells
letterSize = 30
def markLetter(j, i, letter):
    x = cellSize * i + 35
    y = cellSize * j + 40
    W.create_text(x, y, font=("Arial", letterSize), text = letter)
    return

# Marking black cells
def markBlack(col, row):
    W.create_rectangle(col * cellSize, row * cellSize, col * cellSize + cellSize, row * cellSize + cellSize, fill='black')
    return

textWidth = 350
# Printing Across clues
def createAcross():
    X.create_text(130,50, font=('Arial',40),text='Across')
    j = 0
    for i in acrossClues:
        X.create_text(30, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + acrossClues[i], width=textWidth)
        j+=40
    return

# Printing Down clues
def createDown():
    X.create_text(450,50,font=('Arial',40),text='Down')
    j = 0
    for i in downClues:
        X.create_text(350, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + downClues[i], width=textWidth)
        j+=40
    return

file = open("file.txt")
content = file.read()

# MAIN Method - Making the GUI ----------------------------------------------------------
# Making the main crossword window
window = tk.Tk()
window.title("New York Times Mini Puzzle - Demo 1")                 # Window title

# Creating a canvas and making a crossword structure
W = tk.Canvas(window,width=cellSize * 5,height=cellSize * 5,highlightbackground='black')
W.place(x=100,y=170)
createTable()                   # Print a 5x5 table

# Name of the group as a tk label
tk.Label(window, font=("Arial", 20), text="APOLLO", bg='black', fg = 'white').place(y = 100, x = 80)

# Print the current date and time
currentDT = datetime.datetime.now()
tk.Label(window, font=("Arial", 20), text = str(currentDT)[0:16], bg='black', fg = 'white',).place(y = 570, x = 180)

# Puzzle Iteration ----------------------------------------------------------------------------------
# While loop to iterate over each letter in the puzzle
i = 0
while i < 25:
    # Find the first cell using its cell id
    indexLetter = 'id="cell-id-' + str(i) + '"'
    index = content.find(indexLetter)
    letter = content[index + (len(indexLetter) + 8):index + (len(indexLetter) + 18)]

    # Find the empty cell and mark it black
    if letter == 'Cell-block':
        row = int(i / 5)
        col = i % 5
        markBlack(col, row)                 # Mark cell black given cell coordinates
        i+=1
        continue
    # If not a black cell, continue with other options
    else:
        # Find the index for the letter in the cell
        index2 = content.find('text-anchor="middle"', index)
        indexStart = content.find('text-anchor="start"', index, index2)
        # If the cell has a number, then print the number on top left corner
        if indexStart != (-1):
            indexNumber = content.find("</text>", indexStart)
            letterNumber = content[indexNumber + 7]
            markNum(int(i / 5), (i % 5), letterNumber)
        index3 = content.find('</text>',index2)
        # Main letter has the letter in the cell
        mainletter = content[index3-1]
        # Print the letter in the center of the cell
        markLetter(int(i / 5), (i % 5), mainletter)
    i+=1

# Clues Section ----------------------------------------------------------------------------
# Create a canvas for the clues
X = tk.Canvas(window,height = 300,width=700,highlightbackground='black')
X.pack(padx=50,side='right')                # Position the clues section canvas at the right side of the screen

# ACROSS SECTION --------------------------------------------------------------------------
# Store the clues in a dictionary, label is clue number, element is clue itself
acrossClues = dict()
index = content.find("Across")
index2 = content.find("</span>", index)
j = 0
# Find each clue and store append it to the 'acrossClues' dictionary
while j < 5:
    clueNumber = content[index2-1]
    indexStart = content.find(">", index2 + 8)
    indexEnd = content.find("<", indexStart)
    acrossClues[clueNumber] = content[indexStart+1:indexEnd]
    index2 = content.find("</span>", indexEnd + 10)
    j+=1
createAcross()              #  Print the across clues section

# DOWN SECTION -----------------------------------------------------------------------------
# Store the clues in a dictionary, label is clue number, element is clue itself
downClues = dict()
index = content.find("Down", indexEnd)
index2 = content.find("</span>", index)
k = 0
# Find each clue and store append it to the 'downClues' dictionary
while k < 5:
    clueNumber = content[index2-1]
    indexStart = content.find(">", index2 + 8)
    indexEnd = content.find("<", indexStart)
    downClues[clueNumber] = content[indexStart+1:indexEnd]
    index2 = content.find("</span>", indexEnd + 10)
    k+=1
createDown()                #  Print the down clues section

# Size of the window
window.geometry("1366x768")
# Main loop runs the GUI itself
window.mainloop()
