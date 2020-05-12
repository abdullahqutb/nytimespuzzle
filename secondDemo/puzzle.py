# Import the tkinter library for the gui
import tkinter as tk
# Import Selenium libraries and relevant drivers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

class puzzle:
    CELL_SIZE = 75
    NUM_CELL = 5

    def __init__(self):
        # Getting the data from New York Times puzzle - SELENIUM ---------------------------------
        # Main driver for Selenium opening Firefox
        driver = webdriver.Firefox()

        driver.set_page_load_timeout(50)                                            # Timeout after 50secs if page does not load
        driver.get("https://www.nytimes.com/crosswords/game/mini")                  # Open the new york times website
        driver.find_element_by_xpath("//button[@aria-label='OK']").send_keys(Keys.ENTER)        # Press Enter right after the website opens up
        driver.find_element_by_xpath("//button[@aria-label='reveal']").click()                     # Click on Reveal to open the reveal sub menu
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a').click()
        driver.find_element_by_xpath("//button[@aria-label='Reveal']").send_keys(Keys.ENTER)            # Press Enter to reveal the puzzle
        driver.find_element_by_xpath("//button[@aria-label='Subscribe to Play']").send_keys(Keys.ENTER)         # Press enter to close the pop up
        element = driver.find_element_by_xpath("/html/body")            # Put the body tag inside element
        time.sleep(2)                   # Wait 4secs after loading is finished
        content = element.get_attribute("innerHTML")       # Copy all html to word
        time.sleep(2)                   # Wait 4secs after loading is finished
        driver.quit()                 # Quit the driver and session

        # file = open("file.txt", "r")
        file = open("file.txt", "w+")
        # content = file.read()                                # Read the file to content
        # # print(content)
        file.write(content)                                # Write all html to file
        file.close()

        self.createGUI(content)

        window.geometry("1366x768")
        window.mainloop()

        return

    # Creating the grid table of the puzzle
    def createTable(self):
        i = 0
        while i <= self.NUM_CELL * self.CELL_SIZE:
            j = 0
            while j <= self.NUM_CELL * self.CELL_SIZE:
                W.create_rectangle(i, j, self.CELL_SIZE, self.CELL_SIZE, outline='black')
                j+=self.CELL_SIZE
            i+=self.CELL_SIZE
        return

    # Marking numbers based on clues
    def markNum(self, j, i, num):
        x = cellSize * i + 10
        y = cellSize * j + 12
        W.create_text(x, y, font=("Arial", 15), text = num)
        return

    # Writing letters in cells
    def markLetter(self, j, i, letter):
        x = cellSize * i + 35
        y = cellSize * j + 40
        W.create_text(x, y, font=("Arial", 30), text = letter)
        return

    # Marking black cells
    def markBlack(self, col, row):
        cellSize = self.CELL_SIZE
        W.create_rectangle(col * cellSize, row * cellSize, col * cellSize + cellSize, row * cellSize + cellSize, fill='black')
        return

    textWidth = 350
    # Generating Across clues
    def createAcross(self):
        X.create_text(130,50, font=('Arial',40),text='Across')
        j = 0
        for i in acrossClues:
            X.create_text(30, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + acrossClues[i], width=textWidth)
            j+=40
        return

    # Generating Down clues
    def createDown(self):
        X.create_text(450,50,font=('Arial',40),text='Down')
        j = 0
        for i in downClues:
            X.create_text(350, 100 + j,font=('Arial',12), anchor='w', text= i + ": " + downClues[i], width=textWidth)
            j+=40
        return

    def createGUI(self, content):
        # MAIN Method - Making the GUI ----------------------------------------------------------
        # Making the main crossword window
        window = tk.Tk()
        window.title("New York Times Mini Puzzle - Demo 1")

        #creating a canvas and making a crossword structure
        W = tk.Canvas(window,width=self.CELL_SIZE * 5,height=self.CELL_SIZE * 5,highlightbackground='black')
        W.place(x=100,y=170)
        self.createTable()

        # Name of the group as a tk label
        tk.Label(window, font=("Arial", 20), text="Group: APOLLO", bg='black', fg = 'white').place(y = 100, x = 80)

        # Print the current date and time
        currentDT = datetime.datetime.now()
        tk.Label(window, font=("Arial", 20), text = "Date: " + str(currentDT)[0:16], bg='black', fg = 'white',).place(y = 570, x = 180)

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
        return


myPuzzle = puzzle()
