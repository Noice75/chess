import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import time
import bot
import threading
import random

driver = None
b = []
bruh = None

played = 0
win = 0
stop = False
wait = False

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\\Users\\UwU\\AppData\\Local\\Google\\Chrome\\User Data")
driver = uc.Chrome(options=chrome_options)

def checkWin():
    global win
    global played
    global stop
    while True:
        try:
            if('You Won!' in WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="header-title-component"]')))[-1].text):
                win += 1
                played += 1
                stop = True
                print(f'Wins = {win}, Lost = {played-win}, Played = {played}')
                with open('status.json','w') as file:
                    data = json.dumps({'win':win,'played':played,'lost':played-win},indent=4)
                    file.write(data)
                time.sleep(5)
                while wait:
                    time.sleep(1)
                
            else:
                played += 1
                stop = True
                print(f'Wins = {win}, Lost = {played-win}, Played = {played}')
                with open('status.json','w') as file:
                    data = json.dumps({'win':win,'played':played,'lost':played-win},indent=4)
                    file.write(data)
                time.sleep(5)
                while wait:
                    time.sleep(1)
        except:
            pass
checkWinThread = threading.Thread(target=checkWin)
checkWinThread.start()

def getColor():
    try:
        WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"square-12")]')))[-1].click()
        WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"hint square-13")]')))
        WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"square-12")]')))[-1].click()
        color = 'black'
    except:
        color = 'white'
    print('Their Color = ',color)
    return color

def start():
    global bruh
    global stop
    stop = False
    driver.maximize_window()
    driver.get('https://www.chess.com/play/online/new')
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="ui_v5-button-component ui_v5-button-primary ui_v5-button-large ui_v5-button-full"]')))[0].click() #play
    while True:
        try:
            print('Started ? ',len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"connection-component")]')))) > 1)
            if(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"connection-component")]')))) > 1):
                break
        except:
            continue
    bruh = getColor()
    bot.gameStart(bruh)

def owo():
    try:
        if(stop):
            return True
        hi = WebDriverWait(driver,100).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"highlight square-")]')))
        a = []
        for i in hi:
            a.append(i.get_attribute("class").split("-")[-1])
        if(len(WebDriverWait(driver,1).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{a[0]}")]')))) > 1):
            movedFrom = a[1]
            movedTo = a[0]
        else:
            movedFrom = a[0]
            movedTo = a[1]
        return movedFrom,movedTo
    except:
        pass

def move(moveFrom,moveTo):
    print(f"Trying to move from {moveFrom} to {moveTo} - player side")
    try:
        try:
            WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"square-{moveFrom}")]')))[-1].click()
        except:
            if(bruh == 'white'):
                WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="promotion-piece bq"]')))[-1].click()
            else:
                WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="promotion-piece wq"]')))[-1].click()

        x = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[contains(@class,"hint square-{moveTo}")]')))
        for i in x:
            print(i.get_attribute("class"), f'square-{moveTo}' in i.get_attribute("class"))
            if(f'square-{moveTo}' in i.get_attribute("class")):
                x = i
                break
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(x,5,5)
        action.click()
        action.perform()
        while owo() == (moveTo,moveFrom):
            continue
        while owo() == (moveFrom,moveTo):
            continue
        return owo()
    except:
        pass

def game():
    global b
    while True:
        try:
            if(bruh == 'white'):
                a = owo()
                if(a == True):
                    break
                if(a != b):
                    print(f"Moved from {a[0]} to {a[1]} - player side")
                    x = bot.move(a[0],a[1])
                    move(x[0],x[1])
                    b = a
            else:
                a = bot.owo()
                if(a == True):
                    break
                if(a != b):
                    print(f"Moved from {a[0]} to {a[1]} - player side")
                    x = move(a[0],a[1])
                    print(f"Moved from {x[0]} to {x[1]} - bot side")
                    bot.move(x[0],x[1])
                    b = a
        except:
            if(owo() == True):
                    break
            else:
                print("Error!")

while True:
    wait = True
    bot.reset()
    start()
    wait = False
    game()
    print("Resetting!")