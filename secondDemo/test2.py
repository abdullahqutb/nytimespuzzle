# Instructions to run--------------------------------------------------------------------------------------
# In ubuntu/linux:
# Make sure to install python3 and Mozilla Firefox in your environment
# Open Terminal in the directory this file is located in
# Type: python3 guiFinal.py
# Instructions to run --------------------------------------------------------------------------------------

# @desc: This program generates clues for the given data filename "file.txt"
#
#
# @author: APOLLO
# @date: 21/04/2020
# @version: v2.0
#

# Import the tkinter library for the gui
import tkinter as tk
# Import Selenium libraries and relevant drivers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os


def oxford(word, a):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.oxfordlearnersdictionaries.com/")
    driver.find_element_by_id("q").send_keys(word)
    time.sleep(1)
    driver.find_element_by_id("q").send_keys(Keys.ENTER)

    try:
        element = driver.find_element_by_class_name("def")
        defi = element.get_attribute("innerHTML")
    except:
        finder(word, a)
        driver.quit()
        return
    result = ""
    stop = defi.find(".")
    in1 = defi.find("<a")
    if(stop != -1 and stop < in1):

        driver.quit()
        return result

    result = defi[:in1]
    in2 = defi.find('ndv">', in1)
    in3 = defi.find('</span', in2)
    in4 = defi.find('/a>', in3)
    result = result + defi[in2+5:in3]
    result = result + defi[in4+3:]

    if(a == 0):
        acrossCluesNew.append(result)
    else:
        downCluesNew.append(result)
    driver.quit()
    return


# def finder(word, a):
#     driver = webdriver.Firefox()
#     time.sleep(2)
#     driver.implicitly_wait(10)
#     driver.set_page_load_timeout(50)
#     driver.get("https://wordfinder.yourdictionary.com/unscramble/")
#     driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(word)
#     time.sleep(1)
#     driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(Keys.ENTER)
#     time.sleep(1)
#     try:
#         element = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/section/div[2]/div[1]/div/div[2]/div[1]/a")
#         defi = element.get_attribute("innerHTML")
#     except:
#         if(a == 0):
#             acrossCluesNew.append("Similar to: ")
#         else:
#             downCluesNew.append("Similar to: ")
#         driver.quit()
#         return
#     if(a == 0):
#         acrossCluesNew.append("Similar to: " + defi)
#     else:
#         downCluesNew.append("Similar to: " + defi)
#     driver.quit()
#     return

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

textWidth = 320
def createAcrossNew():
    # a = newClues.coords(newClues)
    # window.update()
    # x = newClues.winfo_x()
    # y = newClues.winfo_y()
    # print(x)
    # print(y)
    newClues.create_text(130, 50, font=('Arial',40),text='Across')
    j = 0
    k = 0
    for i in acrossClues:
        newClues.create_text(30, 100 + j,font=('Arial',10), anchor='w', text= i + ": " + acrossCluesNew[k], width=textWidth)
        j+=40
        k+=1
    return

# Printing Across clues
def createAcross():
    X.create_text(130,50, font=('Arial',40),text='Across')
    j = 0
    for i in acrossClues:
        X.create_text(30, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + acrossClues[i], width=textWidth)
        j+=40
    return

def createDownNew():
    newClues.create_text(450,50,font=('Arial',40),text='Down')
    j = 0
    k = 0
    for i in downClues:
        newClues.create_text(350, 100 + j,font=('Arial',10), anchor='w', text= i + ": " + downCluesNew[k], width=textWidth)
        j+=40
        k+=1
    return

# Printing Down clues
def createDown():
    X.create_text(450,50,font=('Arial',40),text='Down')
    j = 0
    for i in downClues:
        X.create_text(350, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + downClues[i], width=textWidth)
        j+=40
    return

# file = open("file.txt")
# content = file.read()

# Getting the data from New York Times puzzle - SELENIUM ---------------------------------
# Main driver for Selenium opening Firefox
driver = webdriver.Firefox()

driver.set_page_load_timeout(50)                                            # Timeout after 50secs if page does not load
driver.get("https://www.nytimes.com/crosswords/game/mini")                  # Open the new york times website
driver.find_element_by_xpath("//button[@aria-label='OK']").send_keys(Keys.ENTER)        # Press Enter right after the website opens up
driver.find_element_by_xpath("//button[@aria-label='reveal']").click()                     # Click on Reveal to open the reveal sub menu
driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a').click()     # Click the Puzzle from sub menu
driver.find_element_by_xpath("//button[@aria-label='Reveal']").send_keys(Keys.ENTER)            # Press Enter to reveal the puzzle
driver.find_element_by_xpath("//button[@aria-label='Subscribe to Play']").send_keys(Keys.ENTER)         # Press enter to close the pop up
element = driver.find_element_by_xpath("/html/body")            # Put the body tag inside element
time.sleep(2)                   # Wait 4secs after loading is finished
content = element.get_attribute("innerHTML")       # Copy all html to word
time.sleep(2)                   # Wait 4secs after loading is finished
driver.quit()                 # Quit the driver and session


nFile = open("file.txt", "w+")
nFile.write(content)

# MAIN Method - Making the GUI ----------------------------------------------------------
# Making the main crossword window
window = tk.Tk()
window.title("New York Times Mini Puzzle - Demo 1")                 # Window title
# Size of the window
window.geometry("1366x768")

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
solutionsAcross = list()
solutionsDown = ["", "", "", "", ""]
aLen = 0
dLen = 0
i = 0
wordAcross = ""
wordDown = ""
downIndex = 0
flag = 1
while i < 25:
    indexLetter = 'id="cell-id-' + str(i) + '"'
    index = content.find(indexLetter)
    letter = content[index + (len(indexLetter) + 8):index + (len(indexLetter) + 18)]

    if(len(solutionsAcross) < 5 and aLen == 5):
        solutionsAcross.append(wordAcross)
        aLen = 0
        wordAcross = ""
        downIndex = 0
    if letter == 'Cell-block':
        row = int(i / 5)
        col = i % 5
        markBlack(col, row)
        if (len(wordAcross) > 1 and i > 0 and len(solutionsAcross) < 5 or len(solutionsDown) < 5):
            if (len(solutionsDown) < 5):
                solutionsDown.append(wordDown)
        i+=1
        downIndex+=1
        aLen+=1
        dLen+=1
        if (row == 0 and col == 0):
            blackBlocks.append(1)
        if (row == 0 and col == 1):
            blackBlocks.append(2)
        if (row == 0 and col == 2):
            blackBlocks.append(3)
        if (row == 0 and col == 3):
            blackBlocks.append(4)
        continue
    else:
        index2 = content.find('text-anchor="middle"', index)
        indexStart = content.find('text-anchor="start"', index, index2)
        if indexStart != (-1):
            indexNumber = content.find("</text>", indexStart)
            letterNumber = content[indexNumber + 7]
            markNum(int(i / 5), (i % 5), letterNumber)
            wKey = letterNumber
        index3 = content.find('</text>',index2)
        mainletter = content[index3-1]

        if ((i % 5) == 0 and i > 0):
            downIndex = 0
        wordAcross = wordAcross + mainletter
        aLen+=1
        if (i < 25):
            if (downIndex < 6):
                solutionsDown[downIndex] = solutionsDown[downIndex] + mainletter
                downIndex+=1
        markLetter(int(i / 5), (i % 5), mainletter)


    i+=1

if(len(wordAcross) > 0 and len(solutionsAcross) < 5):
    solutionsAcross.append(wordAcross)
print(solutionsAcross)
print(solutionsDown)


# Clues Section ----------------------------------------------------------------------------
# Create a canvas for the clues
X = tk.Canvas(window,height = 300,width=700,highlightbackground='black')
X.place(x = 550, y = 50)
tk.Label(window, font=("Arial", 20), text = 'Old Clues', bg='black', fg = 'white',).place(y = 25, x = 900, anchor="center")
# X.pack(padx=50,side='right')                # Position the clues section canvas at the right side of the screen

# New clues section
newClues = tk.Canvas(window,height = 300,width=700,highlightbackground='black')
newClues.place(x = 550, y = 400)
tk.Label(window, font=("Arial", 20), text = 'New Clues', bg='black', fg = 'white',).place(y = 375, x = 900, anchor="center")

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

# Update GUI after old clues are loaded
window.after(2000, lambda: window.quit())
window.mainloop()


# Getting NEW Across clues ------------------------------------------------------------------
# Getting Across clues ------------------------------------------------------------------
driverAcross = webdriver.Firefox()
i = 0
acrossCluesNew = list()
while i < 5:
    time.sleep(1)
    driverAcross.implicitly_wait(10)
    driverAcross.set_page_load_timeout(50)
    driverAcross.get("https://www.dictionary.com/")
    driverAcross.find_element_by_id("searchbar_input").send_keys(solutionsAcross[i])
    time.sleep(1)                   # Wait 4secs after loading is finished
    driverAcross.find_element_by_id("searchbar_input").send_keys(Keys.ENTER)

    try:
        element = driverAcross.find_element_by_css_selector("section.css-pnw38j:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        temp = element.get_attribute("innerHTML")       # Copy all html to word
    except:
        oxford(solutionsAcross[i], 0)
        i+=1
        continue
    time.sleep(1)                   # Wait 1sec after loading is finished
    indexDiv = temp.find('one-click-content')
    index1 = temp.find(">", indexDiv)
    index2 = temp.find("<", index1+5)
    clue = temp[index1+1:index2-1]

    acrossCluesNew.append(clue)
    i+=1

driverAcross.quit()                 # Quit the driver and session
createAcrossNew()
window.update()


# Getting Down clues ------------------------------------------------------------------
driverDown = webdriver.Firefox()
i = 0
downCluesNew = list()
while i < 5:
    time.sleep(2)
    driverDown.implicitly_wait(10)
    driverDown.set_page_load_timeout(70)
    driverDown.get("https://www.dictionary.com/")
    driverDown.find_element_by_id("searchbar_input").send_keys(solutionsDown[i])
    time.sleep(1)                   # Wait 4secs after loading is finished
    driverDown.find_element_by_id("searchbar_input").send_keys(Keys.ENTER)

    try:
        element = driverDown.find_element_by_css_selector("section.css-pnw38j:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        temp = element.get_attribute("innerHTML")       # Copy all html to word
    except:
        oxford(solutionsDown[i], 1)
        i+=1
        continue
    time.sleep(1)                   # Wait 4secs after loading is finished
    indexDiv = temp.find('one-click-content')
    index1 = temp.find(">", indexDiv)
    index2 = temp.find("<", index1+5)
    index3 = temp.find("span", index1)
    if index3 != -1:
    clue = temp[index1+1:index2-1]

    downCluesNew.append(clue[:90])
    i+=1

driverDown.quit()
# print(downCluesNew)
createDownNew()
window.update()

for i in acrossCluesNew:
    print(i)
for i in downCluesNew:
    print(i)

# Update the GUI
window.update()
# Start the GUI Loop
window.mainloop()
