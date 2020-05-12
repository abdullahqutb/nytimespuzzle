# Import Selenium libraries and relevant drivers
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os
from bs4 import BeautifulSoup
import requests

def definitions(word):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.definitions.net/")
    driver.find_element_by_id("search").send_keys(word)
    time.sleep(1)
    driver.find_element_by_id("page-word-search-button").send_keys(Keys.ENTER)

    page_link = "https://www.definitions.net/definition/" + word
    page_response = requests.get(page_link, timeout=5)
    print(page_response.content)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    defs = page_content.findAll("p", {"class": "desc"})
    for i in defs:
        print(i.text)
    # print(defs)
    # if(a == 0):
    #     print(defs[0])
    #     acrossCluesNew.append(defs[0])
    # else:
    #     print(result[:100])
    #     downCluesNew.append(defs[0])
    # # driver.quit()
    return


def collinsDict(word):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.collinsdictionary.com/")
    element = driver.find_element_by_css_selector(".search-input").send_keys(word)

    # driver3.find_element_by_xpath("//div[@aria-label='Any time']/div[@class='mn-hd-txt' and text()='Search term']").send_keys(word);
    time.sleep(1)                   # Wait 4secs after loading is finished
    driver.find_element_by_css_selector(".search-input").send_keys(Keys.ENTER)
    # driver3.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div[2]/input").send_keys(Keys.ENTER)
    # driver3.find_element_by_id("searchbar_input").send_keys(Keys.ENTER)
    # driver3.find_element_by_class_name("search-input-container").send_keys(word)
    return

def merriam(word):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.merriam-webster.com/")
    driver.find_element_by_id("s-term").send_keys(word)
    time.sleep(1)
    driver.find_element_by_id("s-term").send_keys(Keys.ENTER)

    return

def oxford(word):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://www.oxfordlearnersdictionaries.com/")
    driver.find_element_by_id("q").send_keys(word)
    time.sleep(1)
    driver.find_element_by_id("q").send_keys(Keys.ENTER)

    element = driver.find_element_by_class_name("def")
    defi = element.get_attribute("innerHTML")
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

    return result

def finder(word):
    driver = webdriver.Firefox()
    time.sleep(2)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(50)
    driver.get("https://wordfinder.yourdictionary.com/unscramble/")
    driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(word)
    time.sleep(1)
    driver.find_element_by_css_selector("#blue_scrabble_search_input").send_keys(Keys.ENTER)
    time.sleep(1)
    element = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/section/div[2]/div[1]/div/div[2]/div[1]/a")
    defi = element.get_attribute("innerHTML")

    print(defi)
    result = ""

    return result

# collinsDict("hello")
# merriam("hell")
# word = finder("sony")
word = "sony"
definitions(word)
