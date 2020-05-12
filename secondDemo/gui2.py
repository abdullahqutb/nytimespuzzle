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
        return
    result = ""
    stop = defi.find(".")
    in1 = defi.find("<a")
    if(stop != -1 and stop < in1):
        result = defi[:stop]
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
    return


def finder(word, a):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://wordfinder.yourdictionary.com/unscramble/")
    driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(word)
    time.sleep(1)
    driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        element = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/section/div[2]/div[1]/div/div[2]/div[1]/a")
        defi = element.get_attribute("innerHTML")
    except:
        if(a == 0):
            acrossCluesNew.append("Similar to: ")
        else:
            downCluesNew.append("Similar to: ")
        return

    if(a == 0):
        acrossCluesNew.append("Similar to: " + defi)
    else:
        downCluesNew.append("Similar to: " + defi)

    return

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
# Generating Across clues
def createAcross():
    X.create_text(130,50, font=('Arial',40),text='Across')
    j = 0
    for i in acrossClues:
        X.create_text(30, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + acrossClues[i], width=textWidth)
        j+=40
    return
def createAcrossNew():
    # a = newClues.coords(newClues)
    window.update()
    x = newClues.winfo_x()
    y = newClues.winfo_y()
    print(x)
    print(y)
    newClues.create_text(130, 50, font=('Arial',40),text='Across')
    j = 0
    for i in acrossCluesNew:
        newClues.create_text(30, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + acrossCluesNew[i], width=textWidth)
        j+=40
    return

def createDownNew():
    newClues.create_text(450,50,font=('Arial',40),text='Down')
    j = 0
    for i in downCluesNew:
        newClues.create_text(350, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + downCluesNew[i], width=textWidth)
        j+=40
    return

# Generating Down clues
def createDown():
    X.create_text(450,50,font=('Arial',40),text='Down')
    j = 0
    for i in downClues:
        X.create_text(350, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + downClues[i], width=textWidth)
        j+=40
    return

# MAIN Method - Making the GUI ----------------------------------------------------------
# Making the main crossword window
window = tk.Tk()
window.title("New York Times Mini Puzzle - Demo 1")

#creating a canvas and making a crossword structure
W = tk.Canvas(window,width=cellSize * 5,height=cellSize * 5,highlightbackground='black')
W.place(x=100,y=170)
createTable()

# Name of the group as a tk label
tk.Label(window, font=("Arial", 20), text="Group: APOLLO", bg='black', fg = 'white').place(y = 100, x = 80)

currentDT = datetime.datetime.now()
tk.Label(window, font=("Arial", 20), text = "Date: " + str(currentDT)[0:16], bg='black', fg = 'white',).place(y = 570, x = 180)

file = open("file.txt", "r")
# file = open("file.txt", "w+")
content = file.read()                                # Read the file to content
# print(content)
# file.write(content)                                # Write all html to file
file.close()


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

# Getting Across clues ------------------------------------------------------------------
driver = webdriver.Firefox()
i = 0
acrossCluesNew = list()
while i < 5:
    time.sleep(1)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.dictionary.com/")
    driver.find_element_by_id("searchbar_input").send_keys(solutionsAcross[i])
    time.sleep(1)                   # Wait 4secs after loading is finished
    driver.find_element_by_id("searchbar_input").send_keys(Keys.ENTER)

    # element = driver.find("/html/body")
    # element = driver.find_element_by_xpath('//*[text()="<div value="1""')
    try:
        element = driver.find_element_by_css_selector("section.css-pnw38j:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        temp = element.get_attribute("innerHTML")       # Copy all html to word
    except:
        oxford(solutionsAcross[i], 0)
        i+=1
        continue
    time.sleep(1)                   # Wait 4secs after loading is finished
    indexDiv = temp.find('one-click-content')
    index1 = temp.find(">", indexDiv)
    index2 = temp.find("<", index1+5)
    clue = temp[index1+1:index2-1]

    acrossCluesNew.append(clue)
    i+=1

driver.quit()                 # Quit the driver and session

createAcrossNew()
# print(acrossCluesNew)

# Getting Down clues ------------------------------------------------------------------
driver2 = webdriver.Firefox()
i = 0
downCluesNew = list()
while i < 5:
    time.sleep(2)
    driver2.implicitly_wait(10)
    driver2.set_page_load_timeout(50)
    driver2.get("https://www.dictionary.com/")
    driver2.find_element_by_id("searchbar_input").send_keys(solutionsDown[i])
    time.sleep(1)                   # Wait 4secs after loading is finished
    driver2.find_element_by_id("searchbar_input").send_keys(Keys.ENTER)

    # element = driver2.find("/html/body")
    # element = driver2.find_element_by_xpath('//*[text()="<div value="1""')
    try:
        element = driver2.find_element_by_css_selector("section.css-pnw38j:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
        temp = element.get_attribute("innerHTML")       # Copy all html to word
    except:
        oxford(solutionsAcross[i], 1)
        i+=1
        continue
    time.sleep(1)                   # Wait 4secs after loading is finished
    indexDiv = temp.find('one-click-content')
    index1 = temp.find(">", indexDiv)
    index2 = temp.find("<", index1+5)
    clue = temp[index1+1:index2-1]

    downCluesNew.append(clue)
    i+=1

driver2.quit()
# print(downCluesNew)
createDownNew()

for i in cluesAcross:
    print(i)
for i in cluesDown:
    print(i)
for i in solutionsDown:
    print("%s" % (i))
# Clues Section ----------------------------------------------------------------------------
X = tk.Canvas(window,height = 300,width=700,highlightbackground='black')
X.pack(padx=50,side='right')

# ACROSS SECTION --------------------------------------------------------------------------
acrossClues = dict()
index = content.find("Across")
index2 = content.find("</span>", index)
j = 0
while j < 5:
    clueNumber = content[index2-1]
    indexStart = content.find(">", index2 + 8)
    indexEnd = content.find("<", indexStart)
    acrossClues[clueNumber] = content[indexStart+1:indexEnd]
    index2 = content.find("</span>", indexEnd + 10)
    j+=1
createAcross()

# DOWN SECTION -----------------------------------------------------------------------------
downClues = dict()
index = content.find("Down", indexEnd)
index2 = content.find("</span>", index)
k = 0
while k < 5:
    clueNumber = content[index2-1]
    indexStart = content.find(">", index2 + 8)
    indexEnd = content.find("<", indexStart)
    downClues[clueNumber] = content[indexStart+1:indexEnd]
    index2 = content.find("</span>", indexEnd + 10)
    k+=1

createDown()

window.geometry("1366x768")
window.mainloop()
